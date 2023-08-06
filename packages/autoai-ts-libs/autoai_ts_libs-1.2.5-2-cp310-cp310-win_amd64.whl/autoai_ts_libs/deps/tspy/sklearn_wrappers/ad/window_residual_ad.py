#
# IBM Confidential
#
# OCO Source Materials
#
# (c) Copyright IBM Corp. 2022
#
# The source code for this program is not published or otherwise divested of
# its trade secrets, irrespective of what has been deposited with the U.S.
# Copyright Office.
#
import copy
import pickle

import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted, check_array

from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator

import autoai_ts_libs.deps.tspy
from autoai_ts_libs.deps.tspy.sklearn_wrappers.utils.ad_utils import WatForeADUtils
from autoai_ts_libs.deps.tspy.sklearn_wrappers.utils.ad_utils import (RUNMODE_TEST)
import logging

logger = logging.getLogger(__name__)
logger.setLevel('WARNING')

EXOGENOUS_MODELS = WatForeADUtils.get_exogenous_modelnames()

class WindowedResidualAnomalyDetector(BaseEstimator):

    """g
    Pointwise anomaly detection is based on Statistical Forecasting models. It detects anomaly based on forecasted
    value outside confidence intervals at defined confidence level. This anomaly detection will use provided model,
    which is trained and then used to mark anomalies.
    The forecasting model should be trained outside the anomaly detector i.e., detector uses pre-trained model.

    The provided forecasting model must support boundsAt() which is used to computed bounds/confidence intervals at
    certain confidence level.
    """
#model, IWindowedAnomalyDetector detector
    def __init__(self, confidence_interval=0.95, algorithm='hw', algorithm_type = 'additive', ts_icol_loc=-1,
                 k_nearest_windows = 1, min_windows = 2,regular_interval = 1, window_size = 4, history_length = -1,
                 interpolator=None, log_transform=False, lookback_win=1, target_column_indices=-1,
                 feature_column_indices = -1, error_history_length = 2, use_full_error_history = False,
                 error_horizon_length = 2,update_with_anomaly=True,run_mode = RUNMODE_TEST, **kwargs):

        self.ts_icol_loc = []#ts_icol_loc # this override is to not provide timestamps to windowed one
        self.target_column_indices = target_column_indices
        self.feature_column_indices = feature_column_indices
        self.exog_column_indices = []  #

        self.debug = False
        self.run_mode = run_mode

        self._timestamps = None
        self._totalsamples = None  # total samples used to train models
        self.lookback_win = lookback_win
        self.log_transform = False # keeping it false as we will need to add reverst transform in predict
        self.n_targets_ = -1
        self.n_features_ = -1 # set to -1 by default

        self.model_family = 'WindowedResidual'
        self.model_name = self.model_family +'_'+algorithm # this model name is for printing purposes
        self.model_description = self.model_name #there can be extra things appeneded to description
        self.algorithm = algorithm #this alogrithm name should not be changed, this is one of the watfore algorithms
        self.algorithm_type = algorithm_type
        self.confidence_interval = confidence_interval
        # flag to tell if anomalous datapoint should be used to update model or not
        self.update_with_anomaly = update_with_anomaly
        #self.forecasting_model = None # this is the instantiated forecasting algorithm(s) trained on data.

        self.model = []
        self.anomaly_detector = []
        self.anomalies_replaced = False # will be set if anomalous datapoints in training data are replaced
        #self.model_dumps = [] # used for pickle/unpickle only
        # These need to be passed down to forecasting models as they are used to computed bounds()
        # and errors inside models needed for anomaly detection

        self.error_history_length = error_history_length
        self.use_full_error_history = use_full_error_history
        self.error_horizon_length = error_horizon_length

        self.history_length = history_length
        self.k_nearest_windows = k_nearest_windows
        self.min_windows = min_windows
        self.regular_interval = regular_interval
        self.window_size = window_size
        self.interpolator = interpolator


        self.all_args = kwargs

        #self.all_args['algorithm'] = self.algorithm
        self.all_args['algorithm'] = self.algorithm

        # if self.forecasting_model is not None: # if model is loaded
        #     self.n_targets_ = self.forecasting_model.n_targets_
        #     self.n_features_ = self.forecasting_model.n_features_

    def get_pipeline_name(self):
        """
        To return unique pipeline name through combining properties
        like algorithm, algorithm_type, package
        The order among these properties might need revision to ensure consistency
        and meeting expectation from Dev side.
        """
        pipeline_name =  "WindowedResidual_" + self.algorithm
        return pipeline_name

    def fit(self, X, y=None, _reset_model=True, **fit_params):


        #Parse data into format that autoai_ts_libs.deps.tspy understnad
        #parse algorith to create appropriate model
        #generate ts if its not there already
        #create multiple models in case of multivariate/multi-target case and keep array of models
        #use ts if it is there
        #train the models via isanomaly
        #print('Labels in fit=====>>',labels)
        labels = y
        if -1 != self.target_column_indices:
            self.n_targets_ = len(self.target_column_indices)
        else:  # case where target_Col index  == -1
            self.n_targets_ = len(X[0])  # #self.feature_column_indices

        if self.model is None:
            self.model = []
            self.anomaly_detector = []
        elif _reset_model: # will not update existing model
            if len(self.anomaly_detector) != 0:
                for m in self.anomaly_detector:
                    m.reset_detector()
            self.model = []  # self._getModel(algorithm=self.algorithm, kw_args=self.all_args)
            self.anomaly_detector = []

        #X = check_array(X, accept_sparse=True, force_all_finite=False)
        X = np.asarray(X)

        if labels is not None:
            labels = check_array(labels, accept_sparse=True, force_all_finite=False)

        # print('Labels in fit=====>>', labels)
        if -1 != self.feature_column_indices and -1 != self.target_column_indices:
            self.exog_column_indices = list(set(self.feature_column_indices) - set(self.target_column_indices))
            if len(self.exog_column_indices) > 0:
                self.n_features_ = len(self.exog_column_indices)

        #find the time column index and extract or generate timestamps
        self._timestamps = []
        ts_col = -1

        if self.ts_icol_loc == -1 or len(self.ts_icol_loc) == 0:
            # autogenerate ts
            len_ts = X.shape[0]
            for t in range(0, len_ts):
                self._timestamps.append(int(t))
        else:
            # print(self.ts_icol_loc[0])
            ts_col = self.ts_icol_loc[0]  # Assuming for now only one timestamp
            if ts_col < 0 or ts_col >= X.shape[1]:
                # self.stop_context()
                # raise RuntimeError(Messages.get_message(str(ts_col), message_id='AUTOAITSLIBS0005E'))
                raise RuntimeError('Timestamp column is out of range.')

            # print(X[:,ts_col])
            ts = X[:, ts_col]  # X[:, :ts_col+1].flatten()
            # print (ts)
            for t in ts:
                self._timestamps.append(WatForeADUtils.get_unixtimestamp(t)) # Assuming LONG format timestamp
            # [X.flatten().tolist()]

        vals_df_array = [] #parsed values
        #labels_df_array = []  # parsed values
        exogenous_matrix = [] # features/exogenous variables
        self._totalsamples = len(self._timestamps) #Assumption atleast timestamp is there even if value is missing
        self.last_exogenous_values = None # for now exogenous with bounds is not supported but may be in future

        if self.exog_column_indices !=-1 and len(self.exog_column_indices ) != 0\
                and len(self.feature_column_indices) > 0:
            # XH: as it can be an empty list [] (see above as well)
            exogenous_matrix = self._get_exogenous_matrix(X, self.exog_column_indices, ts_col)
            self.last_exogenous_values = exogenous_matrix[-1]

        #################################+++++MODEL CREATION Param Setting+++++#########################################
        #This will also populate vals_df_array, if update_anomaly is False, the it also replaces anomalous
        # value with average of non-anomalous values
        WatForeADUtils.generate_ad_models(self,X, ts_col, vals_df_array,labels)
        #print('After labels======',vals_df_array)
        vals_df_array_log = []
        # NOTE This is going to keep original vals for all in case one ts has negative values
        # log of negative is nan so we don't log transform that

        if self.log_transform:
            lg_val = np.log1p(1 + np.array(vals_df_array))
            if np.isnan(lg_val).any():
                self.log_transformed = False
            else:
                vals_df_array = lg_val  # .insert(cnt, lg_val)
                del lg_val

        if self.history_length == -1 or self.history_length < self.k_nearest_windows + self.window_size:
            self.history_length = len(vals_df_array[0])
        ##########################CREATE AD##########################
        for m in self.model:
            #create window anomaly detector
            w_ad = autoai_ts_libs.deps.tspy.forecasters.windowed_knn_anomaly_detector(self.confidence_interval, self.k_nearest_windows,
                                                                 self.min_windows, self.regular_interval,
                                                                 self.window_size, self.history_length,
                                                                 self.interpolator)
            #create residual AD from Window AD and model
            adm = autoai_ts_libs.deps.tspy.forecasters.windowed_residual_anomaly_detector(regular_interval=self.regular_interval,
                                                                      window_size=self.window_size,
                                                                      interpolator=self.interpolator,model=m,
                                                                      anomaly_detector=w_ad)
            self.anomaly_detector.append(adm)
        #################################+++++DONE MODEL CREATION Param Setting+++++####################################
        if self.debug:
            print("==============MODELS Created==============",self.model)
            print(str(self.__class__) + ' fit \n X==' + str(X) + '\n y=' + str(y))

        #print("==============MODELS BOUNDED AD  Created==============", self.model[-1].is_initialized())
        self.train_ad_model(vals_df_array, exogenous_matrix)

        m_fitted_ = True
        # print('After model trained',self.all_args)
        for m in self.model:
            if not m.is_initialized():
                m_fitted_ = False
            # self.model_name = m.getModelName() # not yet available
        if m_fitted_:
            self.is_fitted_ = True
        else:
            if hasattr(self, 'is_fitted_'):
                del self.is_fitted_

        #print("==============MODELS BOUNDED AD  after Training==============",self.is_fitted_ )
        ####################################################++++++++++++++++++++++++++++++++++++########################

        return self

    def train_ad_model(self,vals_df_array,exogenous_matrix=None):
        #########################################Start BULK UPDATE #############################################################
        # print("================",vals_df_array)
        # self.temp_data = vals_df_array
        # for col in range(0, self.n_features_):
       # if self.debug:
       #     print('Labels===',str(labels_df_array))
        ts_l = len(self._timestamps)
        for col in range(0, self.n_targets_):
            try:
                # print(vals_df_array[col].shape)

                if ('arima' == self.algorithm.lower() or
                    'arma' == self.algorithm.lower()) and ts_l > 50:
                    ###################ARIMA varying init size cases############
                    # arima_min_train_size = ts_l
                    model_initialized = False
                    ###########################################################
                    itr = 0
                    # itr > 4 so after 4 tries and arima_min_train_size = -1 exit out of loop even if model is not init
                    while (not model_initialized) and itr < 5:
                        arima_min_train_size = WatForeADUtils.get_arima_init_size(itr, ts_l)
                        itr = itr + 1
                        try:
                            #                            print("ARIMA MIN TRAINING ====== ",arima_min_train_size)
                            self.all_args['min_training_data'] = arima_min_train_size
                            self.model[col] = WatForeADUtils.create_model(caller_self=self,**self.all_args)
                            # another optimization might be to provide latest data only for initialization
                            # This could be tricky since we cannot provide data out of order and will have
                            # difference in provided data length and last update model time(in case of missing timestamp)
                            self.model[col].update_model(self._timestamps, vals_df_array[col].tolist())
                            model_initialized = self.model[col].is_initialized()
                            # print ("MODEL TRAINIGN STATUS=========",model_initialized)
                        except  BaseException as e:
                            er = str(e)
                            raise (Exception(er))
                    self.model[col].reset()# Reset model as we want ad to train it
                    ##############################################################
                # IF NOT ARIMA just Train model
                else:
                    if self.algorithm.lower() in EXOGENOUS_MODELS:
                        # print ('Exo algo target',vals_df_array[col].tolist())
                        # print ('Exo algo feature matrix', exogenous_matrix)
                        #AD NOT Supported Yet.
                        #self.model[col].update_model(vals_df_array[col].tolist(), exogenous_matrix)
                        self.is_exogenous_pipeline_ = True
                        raise (ValueError('AD with Exogenous not implemented!!!!!!!!!!!!!!!!!'))
                    else:
                        #print("Model initialized===",self.model[-1].is_initialized())
                        for i in range(0,len(vals_df_array[col])):
                            self.anomaly_detector[col].is_anomaly(self._timestamps[i],vals_df_array[col][i])
                            #print('updated too',self.model[col].last_time_updated,vals_df_array[col][i])
                            #print("Model initialized===", self.model[-1].is_initialized())
                            #print('Is Anomaly ',b)

            except Exception as e:
                logger.warning(self.all_args)
                # print(e)
                logger.warning("Failed to train Model.")
                raise (Exception(str(e)))  # For Joint Optimizer to continue
            #########################################END BULK UPDATE #############################################################
            vals_df_array[col] = None  # clear up as model training is done.
            #labels_df_array[col] = None

    """
    Checks if given value is within predicted bounds on certain confidence level. If it is outside bounds, it is
    flagged as an anomaly.
    """

    def get_anomaly_flag(self,bounds,value):
        pass

    def anomaly_score(self, X=None, **predict_params):
        print('Anomaly Score not implemented.')

    def predict(self, X=None):

        try:
            #check_is_fitted(self, 'is_fitted_', msg=Messages.get_message(message_id='AUTOAITSLIBS0056E'))
            check_is_fitted(self, 'is_fitted_', msg=' Model not Fitted!!')
        except BaseException as e:
            logger.warning(self.model_description + ' Model not Fitted!!')
            raise (Exception(str(e)))

        pred_timestamps = []
        all_bounds = []
        all_binaryFlags = []
        multi_col_pred_timestamps = []

        vals_df_array = []

        if X.any() != None and X.shape[0] != 0:
            #Make model copy and work on copy so original model stays unchanged
            model_copies = WatForeADUtils.get_models_copy(self.anomaly_detector)


            if self.ts_icol_loc != -1 and len(self.ts_icol_loc)!=0 :
                pred_timestamps = X[:, self.ts_icol_loc]
                pred_timestamps = WatForeADUtils.get_vectorize_unixts()(pred_timestamps )
            else:
                # NO timestamp provided or X is empty or None so do the best you can :-)
                # In case of multi-variate Multiple models might have different last updated timestamp unless update_anomaly = True
                # This brings extra challenge so separate pre_timestamps per model should be maintained, unless user provides
                # timestamps which ensures we don't get past timestamps
                for m_col in range(0, self.n_targets_):
                    prev_ts = self.model[m_col].last_time_updated
                    per_model_ts = []
                    for t in range(0, X.shape[0]):
                        prev_ts = prev_ts + self.model[m_col].average_interval  # assuming model is initialized and non-exogenous
                        # print('TS==', prev_ts,WatForeADUtils.get_train_interval(self),self.model[-1].last_time_updated)
                        per_model_ts.append(prev_ts)
                    multi_col_pred_timestamps.append(per_model_ts)


            for val_ind in range(0, X.shape[1]):
                if ((val_ind not in self.ts_icol_loc) and val_ind in self.target_column_indices):#-1 == self.target_column_indices):
                    vals_df_array.append(X[:, val_ind])
            #print('X.shape[1]= ', vals_df_array)
            #model_cp = WatForeADUtils.get_models_copy(self.model)

            for row in range(0, X.shape[0]):
                per_model_bds = []
                #per_model_flgs = []
                for col in range(0, self.n_targets_):
                    try:
                        #self.model_update_predict[col].update_model(int(pred_timestamps[row]),
                        #                                        float(vals_df_array[col][row]))
                        #print('Predict TS=',int(pred_timestamps[row]), ' Value=',float(vals_df_array[col][row]))
                        #print('===========',col)
                        actual_value = float(vals_df_array[col][row])
                        per_model_bds.append(WatForeADUtils.get_anomaly_label(
                            model_copies[col].is_anomaly(
                                int(pred_timestamps[row]) if len(pred_timestamps) != 0 else int(multi_col_pred_timestamps[col][row])
                                , actual_value)))

                        #print('BOUNDS===>', bnds)
                    except BaseException as e:
                        print('Skipping Update model, current Timestamp', str(pred_timestamps[row]), 'Current Value ',
                          str(vals_df_array[col][row]))
                        print(e)
                all_bounds.append(per_model_bds)
                # for ts in pred_timestamps:
                #     print('Predict TS=', type(ts[-1]))
                #     print('Bounds=', self.forecasting_model.model[0].bounds_at(int(ts[-1]), self.confidence_interval))
            # else:#NO timestamp provided or X is empty or None so do the best you can :-)
            #
            #     for t in range(0, X.shape[0]):
            #         prev_ts = prev_ts + self.forecasting_model.get_train_interval()
            #         print('Predict Auto TS=',prev_ts)
            #         print('Bounds=',self.forecasting_model.model[0].bounds_at(prev_ts, self.confidence_interval))
        else:

            logger.warning("X Cannot be None")
            raise ValueError("X Cannot be None")

        # X Should not be empty as this is not forecasting its scoring for anomaly given a value
        # else:#For cases where X is None or empty
        #     for i in range(0, self.prediction_horizon):
        #         per_model = []
        #         prev_ts = prev_ts + self.forecasting_model.get_train_interval()
        #         print('Predict TS=', prev_ts)

        #print('Provided Predict TS=', pred_timestamps, all_bounds)

        #predicted_values = []
        #timepoint = self.forecasting_model.get_last_updated()
        #print(self.forecasting_model.model[0].bounds_at(timepoint + 1, self.confidence_interval))
        #print('Predicted Values in AD= ', predicted_values)

        #print('ALL Multiple Labels====***', all_bounds)
        single_lables = []
        for labels in all_bounds:
            single_lables.append(WatForeADUtils.majority_vote(labels))
        #print('Single Labels====***', single_lables)
        return np.asarray(single_lables)

    def get_model_params(self):
        return self.all_args

    #Remove these functions one support is added to autoai_ts_libs.deps.tspy
    # def __getstate__(self):
    #     # self.model_dumps = []
    #     # state = self.__dict__.copy()
    #     # for m in self.model:
    #     #   state['model_dumps'].append(pickle.dumps(m))
    #     self.anomaly_detector = []
    #     state = self.__dict__.copy()
    #     return state
    # #
    # def __setstate__(self, state):
    #     self.__dict__.update(state)
    #
    #     # self.model = [] pickle.loads(m)
    #     for m in self.model:
    #         if self.anomalies_replaced:
    #             # since we are givne labels and anomalies_replaced was set we don't want anomaly detctor to
    #             # use its own estimation
    #             adm = autoai_ts_libs.deps.tspy.forecasters.updatable_anomaly_detector(model=m, confidence=self.confidence_interval,
    #                                                               update_anomalies=False)
    #         else:
    #             adm = autoai_ts_libs.deps.tspy.forecasters.updatable_anomaly_detector(model=m, confidence=self.confidence_interval,
    #                                                               update_anomalies=self.update_with_anomaly)
    #         self.anomaly_detector.append(adm)
    #

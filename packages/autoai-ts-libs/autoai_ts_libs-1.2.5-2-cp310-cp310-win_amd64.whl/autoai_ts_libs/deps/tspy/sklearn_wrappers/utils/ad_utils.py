import math
import pickle

import logging
import numpy as np
#from autoai_ts_libs.deps import autoai_ts_libs.deps.tspy

import datetime
from numpy.compat import long
from scipy.special import ndtri
from sklearn.preprocessing import MinMaxScaler
import autoai_ts_libs.deps.tspy
logger = logging.getLogger(__name__)
logger.setLevel('WARNING')

EXOGENOUS_MODELS = {'arimax', 'arimax_palr', 'arimax_rsar', 'arimax_rar', 'arimax_dmlr'}
RUNMODE_BENCHMARK = 'benchmark'
RUNMODE_TEST = 'test'
RUNMODE_INTEGRATION = "integration"
class WatForeADUtils():
    debug = False

    ANOMALY = -1
    NON_ANOMALY = 1
    UNKNOWN_ANOMALY = 0
    MAX_ANOMALY_SCORE = 10000000000
    SCORE_NOISE = 1e-7

    INIT_SAMPLES_PER_MULTIPLIER = 2 # Default 2*seasonal length

    @classmethod
    def get_anomaly_label(cls, flag): #flag is either true or false
        if flag:
            return cls.ANOMALY
        if not flag:
            return cls.NON_ANOMALY


    @classmethod
    def create_model(cls,caller_self, **kw_args):

        #print('create_model')
        """
        Returns model for respective algorithm.
                Parameters
        ----------
        kw_args: all the keyword args contain parameters passed to main caller class, containing all information
        related to creating model.

        :returns
        created model along with model_id and model description



        """

        # print('Forecaster called with ', algorithm,kw_args)
        algorithm = kw_args['algorithm']

        ##Exogenous model params###########################
        ##self, difference_all_data=False, disable_difference=False, diff_eta=False
        difference_all_data = False
        disable_difference = False
        diff_eta = False
        if 'difference_all_data' in kw_args.keys():
            difference_all_data = kw_args['difference_all_data']
        if 'disable_difference' in kw_args.keys():
            disable_difference = kw_args['disable_difference']
        if 'diff_eta' in kw_args.keys():
            diff_eta = kw_args['diff_eta']
        ###Exogenous varaibles###############################
        if 'arimax' == algorithm.lower():
            # parse the parameters
            return autoai_ts_libs.deps.tspy.forecasters.arimax(disable_difference=disable_difference,
                                           difference_all_data=difference_all_data, diff_eta=diff_eta)
        if 'arimax_palr' == algorithm.lower():
            # parse the parameters
            return autoai_ts_libs.deps.tspy.forecasters.arimax_palr(disable_difference=disable_difference,
                                                difference_all_data=difference_all_data, diff_eta=diff_eta)
        if 'arimax_rsr' == algorithm.lower():
            # parse the parameters
            return autoai_ts_libs.deps.tspy.forecasters.arimax_rsr(disable_difference=disable_difference,
                                               difference_all_data=difference_all_data, diff_eta=diff_eta)
        if 'arimax_rar' == algorithm.lower():
            return autoai_ts_libs.deps.tspy.forecasters.arimax_rar(disable_difference=disable_difference,
                                               difference_all_data=difference_all_data, diff_eta=diff_eta)
        if 'arimax_dmlr' == algorithm.lower():
            return autoai_ts_libs.deps.tspy.forecasters.arimax_dmlr(disable_difference=disable_difference,
                                                difference_all_data=difference_all_data, diff_eta=diff_eta)

        ######################################################
        #print(algorithm)
        if 'hw' == algorithm.lower():
            alg_args = {}
            # GOES IN FULL automatic mode finds samples per seaons and init seasons from data and initializes model
            if 'min_training_data' in kw_args.keys():
                # print ('==============',kw_args['min_training_data'] )
                number_of_samples = kw_args['min_training_data']

                if number_of_samples < 1 and kw_args['min_training_data'] >= 0.99:
                    number_of_samples = caller_self._totalsamples
                if number_of_samples < 1 and kw_args['min_training_data'] < 0.99:
                    number_of_samples = int(caller_self._totalsamples * number_of_samples)

                # cap samples used for init
                number_of_samples = min(number_of_samples, 1000000)  # 1Milion
                ###########SET DESCRIPTIONS ETC####
                if 'algorithm_type' not in kw_args.keys():
                    alg_args['algorithm_type'] = 'additive'  # Default is additive
                else:
                    alg_args['algorithm_type'] = kw_args['algorithm_type']

                alg_args['number_of_samples'] = number_of_samples
                alg_args['min_training_data'] = kw_args['min_training_data']
                alg_args['is_season_length'] = False

                #see how to handle this when it comes to re-using this method in watforeforecaster
                if '_' not in caller_self.algorithm or '_' not in caller_self.model_name:  # Daub gives back the same object if not checked it will keep appending
                    caller_self.algorithm = caller_self.algorithm + '_' + alg_args['algorithm_type']
                    caller_self.model_name = caller_self.model_name + '_' + alg_args['algorithm_type']

                caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
                caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)

                ###########################################
                # print('New HW COnstructor ALL ARGS:',alg_args, alg_args['algorithm_type'])
                # print('New COnstructor modelid:', self.model_id)
                return autoai_ts_libs.deps.tspy.forecasters.hws(is_season_length=alg_args['is_season_length'],
                                            number_of_samples=int(alg_args['number_of_samples']),
                                            algorithm_type=alg_args['algorithm_type'])

            # required params

            alg_params = ['samples_per_season', 'initial_training_seasons', 'algorithm_type', 'compute_seasonality'
                , 'error_history_length', 'use_full_error_history']
            for par in alg_params:
                if par in kw_args and kw_args[par] is not None:
                    # print(kw_args[par])
                    # print(par)
                    # print(kw_args[par])
                    if par == 'samples_per_season' or par == 'error_history_length':
                        # print(self.all_args)
                        # print(kw_args[par])
                        if kw_args[par] < 1 and caller_self._totalsamples is not None:
                            # if par == 'samples_per_season' and kw_args[par] > 0.5:
                            if kw_args[par] > 0.5:
                                kw_args[par] = 0.5  # atleast 2 seasons needed i.e., init seasons
                            # alg_args[par] = int(kw_args[par] * self._totalsamples)  # parameters from range
                            alg_args[par] = int(round(kw_args[par] * caller_self._totalsamples, 14))
                            if alg_args[par] <= 0:
                                alg_args[par] = 2

                            # self.all_args[par] = alg_args[par]
                            # print (self.all_args[par])
                        else:
                            alg_args[par] = kw_args[par]

                    else:
                        alg_args[par] = kw_args[par]

                    # self.all_args[par] = alg_args[par]#when fit is called again&again kw_args[par]>1 would force to else block

            if 'samples_per_season' not in alg_args:
                if caller_self._totalsamples is not None:
                    alg_args['samples_per_season'] = int(caller_self._totalsamples * 0.25)
                else:
                    alg_args['samples_per_season'] = 2
                caller_self.all_args['samples_per_season'] = alg_args['samples_per_season']

            if 'initial_training_seasons' not in alg_args:
                if caller_self._totalsamples is not None and alg_args['samples_per_season'] is not None:
                    alg_args['initial_training_seasons'] = int(caller_self._totalsamples / int(alg_args['samples_per_season']))
                else:
                    alg_args[
                        'initial_training_seasons'] = 2  # int(self._totalsamples/int(alg_args['samples_per_season']))#2
                caller_self.all_args['initial_training_seasons'] = alg_args['initial_training_seasons']

            # samples_per_season, initial_training_seasons, algorithm_type="additive", compute_seasonality=None,
            # error_history_length=1, use_full_error_history=True

            # print('=========', caller_self.algorithm_type)
            alg_args['algorithm_type'] = caller_self.algorithm_type
            # if 'algorithm_type' not in alg_args:  # Default is additive
            #     alg_args['algorithm_type'] = 'additive'
            if '_' not in caller_self.algorithm or '_' not in caller_self.model_name:  # Daub gives back the same object if not checked it will keep appending
                caller_self.algorithm = caller_self.algorithm + '_' + alg_args['algorithm_type']
                caller_self.model_name = caller_self.model_name + '_' + alg_args['algorithm_type']

            caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
            caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)
            # print('Non Automatic Mode==',alg_args)
            # print('MODEL ID', self.model_id)
            return autoai_ts_libs.deps.tspy.forecasters.hws(**alg_args)  #

        if 'arima' == algorithm.lower():  #

            alg_args = {}
            # error_horizon_length=1, use_full_error_history=True, force_model=False, min_training_data=-1, p_min=0,
            # p_max=-1, d=-1, q_min=0, q_max=-1

            #################################SET DEFAULTS################
            if 'min_training_data' not in kw_args.keys():
                kw_args[
                    'min_training_data'] = 0.999999  # self._totalsamples-->not good for multiple calls to fit) # Use all of samples for training
            ################################################################
            # optional params
            alg_params = ['error_horizon_length', 'use_full_error_history', 'force_model', 'min_training_data'
                , 'p_min', 'p_max', 'd', 'q_min', 'q_max']

            for par in alg_params:
                if par in kw_args and kw_args[par] is not None:
                    if par == 'error_horizon_length' or par == 'min_training_data':
                        if kw_args[par] < 1 and caller_self._totalsamples is not None:
                            # alg_args[par] = int(kw_args[par] * self._totalsamples)  # parameters from range
                            alg_args[par] = int(
                                round(kw_args[par] * caller_self._totalsamples, 14))  # to convert 7.99999.. to 8
                            if alg_args[par] <= 0:
                                if par == 'min_training_data':
                                    alg_args[par] = -1  # -1 is allowed for Arima
                                else:
                                    alg_args[par] = 2
                            # self.all_args[par] = alg_args[par]#when fit is called again&again kw_args[par]>1 would force to else block
                            # print('error history length ',self.all_args[par])
                        else:
                            alg_args[par] = kw_args[par]
                    else:
                        alg_args[par] = kw_args[par]
            # print('ARIMA ARGS',alg_args)
            caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
            caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)
            return autoai_ts_libs.deps.tspy.forecasters.arima(**alg_args)  #

        if 'arma' == algorithm.lower():  #

            alg_args = {}
            # error_horizon_length=1, use_full_error_history=True, force_model=False, min_training_data=-1, p_min=0,
            # p_max=-1, d=-1, q_min=0, q_max=-1
            if 'min_training_data' not in kw_args.keys():
                kw_args[
                    'min_training_data'] = 0.999999  # self._totalsamples-->not good for multiple calls to fit) # Use all of samples for training
            # optional params
            alg_params = ['min_training_data', 'p_min', 'p_max', 'q_min', 'q_max']

            for par in alg_params:
                if par in kw_args and kw_args[par] is not None:
                    if par == 'min_training_data':
                        if kw_args[par] < 1 and caller_self._totalsamples is not None:
                            # alg_args[par] = int(kw_args[par] * self._totalsamples)  # parameters from range
                            alg_args[par] = int(round(kw_args[par] * caller_self._totalsamples, 14))
                            if alg_args[par] <= 0:
                                if par == 'min_training_data':
                                    alg_args[par] = -1  # -1 is allowed for Arma
                                else:
                                    alg_args[par] = 2
                            # self.all_args[par] = alg_args[par]#when fit is called again&again kw_args[par]>1 would force to else block
                            # print('error history length ',self.all_args[par])
                        else:
                            alg_args[par] = kw_args[par]
                    else:
                        alg_args[par] = kw_args[par]
            # print('ARMA ARGS',alg_args)
            caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
            caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)
            return autoai_ts_libs.deps.tspy.forecasters.arma(**alg_args)  #

        if 'bats' == algorithm.lower():

            alg_args = {}
            # training_sample_size, box_cox_transform = False)
            if 'training_sample_size' not in kw_args.keys():
                kw_args[
                    'training_sample_size'] = 0.999999  # self._totalsamples-->not good for multiple calls to fit)  # 0.999999  # Use all of samples for training

            # optional params
            alg_params = ['training_sample_size', 'box_cox_transform']

            for par in alg_params:
                if par in kw_args and kw_args[par] is not None:
                    if par == 'training_sample_size':
                        if kw_args[par] < 1 and caller_self._totalsamples is not None:
                            # alg_args[par] = int(kw_args[par] * self._totalsamples)
                            alg_args[par] = int(round(kw_args[par] * caller_self._totalsamples, 14))
                            # self.all_args[par] = alg_args[par]#when fit is called again&again kw_args[par]>1 would force to else block
                            # print(alg_args)
                        else:
                            alg_args[par] = kw_args[par]
                    else:
                        alg_args[par] = kw_args[par]

            if 'training_sample_size' not in alg_args.keys():
                if caller_self._totalsamples is not None:
                    alg_args['training_sample_size'] = caller_self._totalsamples
                else:
                    alg_args['training_sample_size'] = 8  # minimum 8 samples are required otherwise it throws error
            caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
            caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)
            # print('ALG Args',alg_args)
            return autoai_ts_libs.deps.tspy.forecasters.bats(**alg_args)  #

        if 'autoforecaster' == algorithm.lower():

            alg_args = {}
            # training_sample_size, box_cox_transform = False)
            # defaults
            if 'training_sample_size' not in kw_args.keys():
                kw_args[
                    'training_sample_size'] = 0.999999  # self._totalsamples-->not good for multiple calls to fit)  # 0.999999  # Use all of samples for training
            if 'min_training_data' not in kw_args.keys():
                kw_args[
                    'min_training_data'] = 0.999999  # self._totalsamples-->not good for multiple calls to fit) # Use all of samples for training
            # optional params
            alg_params = ['min_training_data', 'error_history_length']

            for par in alg_params:
                if par in kw_args and kw_args[par] is not None:
                    if par == 'error_history_length' or par == 'min_training_data':
                        if kw_args[par] < 1 and caller_self._totalsamples is not None:
                            # alg_args[par] = int(kw_args[par] * self._totalsamples)  # parameters from range
                            alg_args[par] = int(round(kw_args[par] * caller_self._totalsamples, 14))
                            if alg_args[par] <= 0:
                                alg_args[par] = 2
                            # self.all_args[par] = alg_args[par] #when fit is called again&again kw_args[par]>1 would force to else block
                        else:
                            alg_args[par] = kw_args[par]
                    else:
                        alg_args[par] = kw_args[par]

            if 'min_training_data' not in alg_args:
                alg_args['min_training_data'] = caller_self._totalsamples  # minimum 8 samples are required otherwise it throws error
                caller_self.all_args['min_training_data'] = alg_args['min_training_data']
            else:
                if alg_args['min_training_data'] < 8:
                    alg_args['min_training_data'] = 8  # minimum 8 samples are required otherwise it throws error
                    # self.all_args['min_training_data'] = alg_args['min_training_data']
            # print(alg_args)
            caller_self.model_id = cls.get_model_id(algorithm, **alg_args)
            caller_self.model_description = caller_self.algorithm + '_' + str(alg_args)
            return autoai_ts_libs.deps.tspy.forecasters.auto(**alg_args)  #

        # Algorithm name not found.
        #raise ValueError(Messages.get_message(message_id='AUTOAITSLIBS0004E'))  # utils needs to be moved to ts_libs
        raise ValueError('Unknown Algorithm')

    def get_last_updated(caller_self, inmodle_array= None):
        last_updated = -1
        EXOGENOUS_MODELS = WatForeADUtils.get_exogenous_modelnames()
        #print(self.model_name)
        #########Special case for exogenous till we make m.last_time_updated available via java models##################
        if caller_self.model_name in EXOGENOUS_MODELS or (not hasattr(caller_self, 'model')):
            if 0 < len(caller_self._timestamps):
                last_updated =caller_self._timestamps[-1]
            return last_updated

        ################################################################################################################
        if inmodle_array is not None:
            for m in inmodle_array:
                if m.is_initialized():
                    # Assuming start training at ts=0 # This would assume multiple time series were update at same time
                    last_updated = m.last_time_updated
                    #print('predict model last updated ', last_updated)
        else:
            for m in caller_self.model:
                if m.is_initialized():
                    last_updated = m.last_time_updated  # Assuming start training at ts=0 # This would assume multiple time series were update at same time

        return last_updated  # starts training at ts=0 unless ts specified

    # Timestamps/sample interval during traing of model
    def get_train_interval(caller_self):
        interval = -1
        EXOGENOUS_MODELS = WatForeADUtils.get_exogenous_modelnames()
        #########Special case for exogenous till we make m.last_time_updated available via java models##################
        if caller_self.model_name in EXOGENOUS_MODELS or (not hasattr(caller_self, 'model')):
            if 1 < len(caller_self._timestamps):
                interval = caller_self._timestamps[-1] - caller_self._timestamps[-2]
            return interval
        ################################################################################################################
        for m in caller_self.model:
            if m.is_initialized():
                interval = m.average_interval  # Assuming start training at ts=0 # This won't work for real ts

        return interval
    @classmethod
    def get_anomaly_fill_val(cls,vals,labels):
        non_anomalous_sum = 0
        count = 0
        for t in range(0, len(labels)):
            if labels[t] != cls.ANOMALY:
                non_anomalous_sum = non_anomalous_sum + vals[t]
                count = count + 1
                if cls.debug:
                    print('Count=',count,' sum=',non_anomalous_sum, ' value ',vals[t] , ' AnomalyFlag=',labels[t])
        if cls.debug:
            print('Mean Vaue ====== ' + str(non_anomalous_sum/count))
        return non_anomalous_sum/count

    # This method can also be moved to some utils for common usage
    def generate_ad_models(caller_self, X, ts_col, vals_df_array, labels=None):
        # Check label if it is present and is anomaly we can replace the value by some stats
        for val_ind in range(0, X.shape[1]):
            if (val_ind != ts_col and -1 == caller_self.target_column_indices) or (-1 != caller_self.target_column_indices and
                                                                            val_ind in caller_self.target_column_indices):

                vals = X[:, val_ind]
                #print('=================BEFOREEEE----',vals)
                if not caller_self.update_with_anomaly and labels is not None and labels.any() != None and len(labels) != 0:
                    # update value to something else
                    # print('=================HERE_----')
                    lbs = labels[:, val_ind]
                    # print('LENGTH', str(len(lbs)))
                    if WatForeADUtils.ANOMALY in lbs:  # this is an array
                        # print('LENGTH====>',str(lbs))
                        # As we already removed anomalies we can go ahead and use these values to udpate models
                        caller_self.anomalies_replaced = True
                        for t in range(0, len(lbs)):
                            if WatForeADUtils.ANOMALY == lbs[t]:
                                # print('Labels ',lbs)
                                # print('vals before====>', str(vals))
                                vals[t] = WatForeADUtils.get_anomaly_fill_val(vals,
                                                                              lbs)  # replace value with mean this far without anomaly
                                # print('vals after Mean Replacement====>', str(vals))

                vals_df_array.append(vals)
                # labels_df_array.append(labels[:, val_ind])
                ts_l = len(caller_self._timestamps)
                #######GET SEASONAL Length############
                # print(self.algorithm)
                # if self.compute_periodicity:
                # For multiple models compute periodicity on each ts and initialize model with that
                # However, when printing the watfore_forecaster object self.all_args['min_training_data']
                # will show last calculated seasonal length, array of values for ['min_training_data'] can be considered
                # but that would require changes in multiple places and would be restricting as we don't know number
                # of ts in advance to define param ranges and sepecify default values.

                # print(X[:,val_ind])
                # print(vals_df_array[-1])

                min_train = caller_self.all_args.get('min_training_data', None)  # if none go to non-auto mode
                # by pass fft analysis if min_train is there meaning automode
                # if (wf.Forecasters.hw == self.algorithm.lower() and min_train is None) or \
                #        'autoforecaster' == self.algorithm.lower() or 'bats' == self.algorithm.lower():
                # by pass fft for hw
                if 'autoforecaster' == caller_self.algorithm.lower() or 'bats' == caller_self.algorithm.lower():
                    # use recently appended ts for seasonality
                    ul = 200  # Max on samples to init
                    ll = 8  # min samples for init, value comes from BATS as it requires minimum 8 samples

                    hw_samps, ac_per, bats_samps, per_fft = WatForeADUtils.get_init_samples(
                        vals_df_array[-1].tolist(),
                        upper_limit=ul,
                        lower_limit=ll)
                    caller_self.all_args['samples_per_season'] = ac_per  # / ts_l #0.5#
                    init_season = int(ts_l / ac_per)  # 2#
                    caller_self.all_args['initial_training_seasons'] = init_season  # fix this to 2 and error goes away
                    # Reset history length according to periodicity in signal
                    # At some point this can be matched with look_back window of other models
                    # print('error histor == ',self.all_args['error_history_length'])
                    # print('error histor == ', self.all_args['error_horizon_length'])
                    # if per == ll / ts_l:  # means get_init_samples returned lower limit then default to 2
                    #    self.all_args['error_history_length'] = 2 / ts_l
                    #    self.all_args['error_horizon_length'] = 2 / ts_l
                    # else:
                if 'error_history_length' not in caller_self.all_args.keys():
                    caller_self.all_args['error_history_length'] = 2  # hw_samps/2
                if 'error_horizon_length' not in caller_self.all_args.keys():
                    caller_self.all_args['error_horizon_length'] = 2  # hw_samps/2# since we double the num samples

                if ('autoforecaster' == caller_self.algorithm.lower() or
                        'bats' == caller_self.algorithm.lower()):
                    caller_self.all_args['min_training_data'] = bats_samps  # Each model gets periodicity computed on its ts
                    caller_self.all_args['training_sample_size'] = bats_samps  # Each model gets periodicity computed on its ts

                    # print (self.all_args['training_sample_size'])
                # print('after init bats samples========',caller_self.all_args)
            ###########################################################
                try:
                    # self.all_args['min_training_data'] might be different for different ts depending seasonal length
                    # print('after init bats samples========',caller_self.all_args, vals)
                    per, multi_season_len = WatForeADUtils.get_regular_season_periodicity(vals)
                    #Override for incremental update/score computation for AD
                    caller_self.all_args['min_training_data'] = WatForeADUtils.INIT_SAMPLES_PER_MULTIPLIER * per  # Each model gets periodicity computed on its ts
                    caller_self.all_args['training_sample_size'] = WatForeADUtils.INIT_SAMPLES_PER_MULTIPLIER * per  # Each model gets periodicity computed on its ts
                    # print('***********',per,caller_self.all_args['training_sample_size'] )
                    caller_self.model.append(WatForeADUtils.create_model(caller_self=caller_self, **caller_self.all_args))
                    if hasattr(caller_self,'scalers'):
                        caller_self.scalers.append(MinMaxScaler()) # initialize scaler per model
                except  BaseException as e:
                    er = str(e)
                    raise (Exception(er))
        return

    def populate_data(caller_self, X, ts_col, vals_df_array, labels=None):
        # Check label if it is present and is anomaly we can replace the value by some stats
        for val_ind in range(0, X.shape[1]):
            if (val_ind != ts_col and -1 == caller_self.target_column_indices) or (
                    -1 != caller_self.target_column_indices and
                    val_ind in caller_self.target_column_indices):

                vals = X[:, val_ind]

                # print('=================BEFOREEEE----')
                if not caller_self.update_with_anomaly and labels is not None and labels.any() != None and len(
                        labels) != 0:
                    # update value to something else
                    # print('=================HERE_----')
                    lbs = labels[:, val_ind]
                    # print('LENGTH', str(len(lbs)))
                    if WatForeADUtils.ANOMALY in lbs:  # this is an array
                        # print('LENGTH====>',str(lbs))
                        # As we already removed anomalies we can go ahead and use these values to udpate models
                        caller_self.anomalies_replaced = True
                        for t in range(0, len(lbs)):
                            if WatForeADUtils.ANOMALY == lbs[t]:
                                # print('Labels ',lbs)
                                # print('vals before====>', str(vals))
                                vals[t] = WatForeADUtils.get_anomaly_fill_val(vals,
                                                                              lbs)  # replace value with mean this far without anomaly
                                # print('vals after Mean Replacement====>', str(vals))

                vals_df_array.append(vals)

        return


    @classmethod
    def majority_vote(cls,anomaly_labels):
        '''
        Computes majority voting i.e., the labels occurs the most and returns that label. In case all are equal we return
        it to be an anomaly.
        :param anomaly_labels: array of anomaly labels 1, 0, -1
        :return: Anomaly flag i.e., 1, 0 or -1. Returns None if empty array is passed.
        '''

        if len(anomaly_labels) ==0 or anomaly_labels is None:
            return None

        anomaly = 0
        non_anomaly = 0
        unkonwn = 0
        max_count  = 0

        final_label = cls.ANOMALY

        for lbl in anomaly_labels:
            if lbl == cls.ANOMALY:
                anomaly += 1
                if max_count <= anomaly:
                    max_count = anomaly
                    final_label = cls.ANOMALY

            elif lbl == cls.NON_ANOMALY:
                non_anomaly += 1
                if max_count < non_anomaly:
                    max_count = non_anomaly
                    final_label = cls.NON_ANOMALY
            elif lbl == cls.UNKNOWN_ANOMALY:
                unkonwn +=1
                if max_count < unkonwn:
                    max_count = unkonwn
                    final_label = cls.UNKNOWN_ANOMALY
            else:
                raise ValueError('Unknown label label=',lbl, ' in the input array')
                return None

        return [final_label]


    @classmethod
    def get_exogenous_modelnames(cls):
        return EXOGENOUS_MODELS
    # This method exists in autoai_tslibs as well
    @classmethod
    def get_arima_init_size(cls, trial_ind, data_len):
        # print ('Data Len == ', data_len)
        data_len_cap = min(data_len, 300000)
        if trial_ind == 4:
            return -1
        else:
            return data_len_cap - int(trial_ind * data_len / 4)

    #Note: Copied from WatforeUtils We might even remove this if model ids are not used
    @classmethod
    def get_model_id(cls, algorithm_name, **params):

        id = 'st_'
        algorithm_type = params.get('algorithm_type', None)
        comput_seasonalty = params.get('compute_seasonality', None)
        box_cox_transform = params.get('box_cox_transform', None)
        use_full_error_history = params.get('use_full_error_history', None)
        force_model = params.get('force_model', None)
        min_training_data = params.get('min_training_data', None)

        number_of_samples = params.get('number_of_samples', None)
        is_season_length = params.get('is_season_length', None)

        if algorithm_name.lower() == 'hw':
            if algorithm_type.lower() == 'additive' and comput_seasonalty == False and \
                    use_full_error_history == False:
                id = id + '1'
            if algorithm_type.lower() == 'multiplicative' and comput_seasonalty == False and \
                    use_full_error_history == None:
                id = id + '2'
            if algorithm_type.lower() == 'additive' and is_season_length == False and number_of_samples is not None:
                id = id + '6'
            if algorithm_type.lower() == 'multiplicative' and is_season_length == False and number_of_samples is not None:
                id = id + '7'

        if algorithm_name.lower() == 'bats' and box_cox_transform == False:
            id = id + '3'
        if algorithm_name.lower() == 'arima' and use_full_error_history == True and \
                force_model == True and min_training_data == -1:
            id = id + '4'
        if algorithm_name.lower() == 'autoforecaster':
            id = id + '5'

        return id


    #Note: Copied from WatforeUtils we might need to move such functions to a common higher util class to avoid duplication
    @classmethod
    def get_init_samples(cls, X, wf_context=None, init_perc=0.25, upper_limit=300,
                         lower_limit=10):

        l = len(X)
        per, all_seasons_lens = cls.get_regular_season_periodicity(X=X, wf_context=wf_context)
        per_from_fft = per
        bats_samps = cls.get_bats_init_samples(l, all_seasons_lens)  # samples to init bats model
        bats_samps = 8 if bats_samps < 8 else bats_samps  # just in case
        # print('PERIORIDICTY==================================== ', per)
        if per != -1:
            # print('number of init samples=', (3*int(per)))
            samples = max(math.ceil(2 * int(per)), lower_limit)  #
            per = int(samples / 2)  # in case lower_limit is selected and to ensure atleast 2 seasons
            ##init_samps = 0.9999 if samples/l == 1 else samples/l
            ############samples for bats##########

            ####################################
            # print('returning SEASONAL ANALYSIS',samples , per,bats_samps,per_from_fft)
            return samples, per, bats_samps, per_from_fft  # 2x the periodicity

        n_samples = max(int(len(X) * init_perc), lower_limit)
        if n_samples > upper_limit:
            n_samples = upper_limit
        # print('PERIORIDICTY==================================== ', per)
        # print('number of init samples=',n_samples)
        # init_samps = 0.9999 if n_samples / l == 1 else n_samples / l
        # print('SEANSONAL Ananlysis Default',n_samples, int(n_samples/2),bats_samps,per_from_fft)
        return n_samples, int(n_samples / 2), bats_samps, per_from_fft  # per

    @classmethod
    def get_regular_season_periodicity(cls, X, wf_context=None, sub_season_percent_delta=0.0,
                                       max_num_seasons=2):
        per = 1
        multi_season_len = None
        try:
        #     if wf_context == None:
        #         import autoai_ts_libs.deps.autoai_ts_libs.deps.tspy as autoai_ts_libs.deps.tspy
        #         # import autoai_ts_libs.deps.tspy
        #         wf_context = autoai_ts_libs.deps.tspy  # autoai_ts_libs.deps.autoai_ts_libs.deps.tspy #TSContext(die_on_exit=False)
            # X = list(np.log1p(100 + np.array(X)))
            season_selector = autoai_ts_libs.deps.tspy.forecasters.season_selector(sub_season_percent_delta)
            multi_season_len = season_selector.get_multi_season_length(max_num_seasons, X)
            # print('seasons==',multi_season_len)
            if len(multi_season_len) > 0:
                multi_season_len.sort()
                per = multi_season_len[-1]  # 0 for smallest season, -1 for largest season
            # print('Period',per)
            # not needed in new autoai_ts_libs.deps.tspy Jan2020
            # if wf == -1:
            #    wf_context.stop()
        except BaseException as e:
            # not needed in new autoai_ts_libs.deps.tspy Jan2020
            # if wf == -1:
            #   wf_context.stop()
            # print(e)
            # logger.warning(Exception(str(e)))
            logger.warning('Cannot find seasons')
        return per, multi_season_len

    @classmethod  # gets runtime from 200sec to 68.40858721733093
    def get_bats_init_samples(cls, num_data_samples, all_seasson_lens):

        # num_data_samples = len(X)
        base_samples = 1000  # This base could be dynamic, if only 1 season is found this can be higher
        up_base_limit = 2200
        MAX_CAP = 300000  # 300K rows
        # per,ac_seas = cls.get_regular_season_periodicity(X=X, wf_context=wf_context)
        if all_seasson_lens is None:
            if num_data_samples <= base_samples:
                return num_data_samples
            else:
                return base_samples

        ac_seas = all_seasson_lens
        ac_seas.sort()  # sort just in case

        if len(ac_seas) <= 1:
            base_samples = up_base_limit
        # else:
        #     if (ac_seas[-1] % ac_seas[0]) == 0:# out of mememory for large datasets
        #         base_samples = 5000

        # print("=================NUM SEASONS========", len(ac_seas))
        # print('Seasons', ac_seas)
        # return int(2*ac_seas[-1])
        if num_data_samples <= base_samples:
            return num_data_samples
        # seas_diff = 0
        # min_samps = 8
        # init_samps = min_samps
        # make sure 2xmax_season samples are available
        if len(ac_seas) == 0:
            seas = 2 # 2xseason length of 1
        else:
            seas = int(2 * ac_seas[-1]) if int(2 * ac_seas[-1]) < num_data_samples else ac_seas[-1]
        # seas = int(2*ac_seas[0]) if int(2*ac_seas[0]) < num_data_samples else ac_seas[0]
        # When there are 2 seasons and 2nd= 2*1st_seasons bats running time can be high for 2*seasonal length
        # if len(ac_seas) > 1:
        #     if (ac_seas[-1] % ac_seas[0]) == 0:
        #         seas = seas + 5 #ac_seas[0]
        lg_in = base_samples + int(num_data_samples / np.log(num_data_samples))
        # check for cases slightly up 3K
        log_inc_samples = lg_in if lg_in < num_data_samples else num_data_samples
        # if len(ac_seas) <= 1 and seas < base_samples :
        #     init_samps = max(seas, log_inc_samples)
        #     print('Num seasons is ', len(ac_seas), init_samps)
        # else:
        init_samps = max(min(seas, log_inc_samples), base_samples)
        # init_samps = min(seas,log_inc_samples)
        # print(' init size as befor limit===', init_samps,ac_seas)
        # check to not cross to 2nd season for init in large ds
        if len(ac_seas) > 1 and num_data_samples > up_base_limit and init_samps > up_base_limit:
            # if init_samps > ac_seas[-1]  and init_samps > up_base_limit:
            init_samps = up_base_limit



        return min(init_samps, MAX_CAP)

    @classmethod
    def get_unixtimestamp(cls, datetime_timestamp):
        unix_ts = 0

        try:
            unix_ts = int(datetime_timestamp)
        except:
            try:
                #This works for 2017-05-02 00:00:00 string format
                datetime_format = datetime.datetime.strptime(datetime_timestamp, '%Y-%m-%d %H:%M:%S')
                unix_ts = datetime.datetime.timestamp(datetime_format)
                #print(int(unix_ts))
            except:
                raise TypeError('Data format conversion not supported')

        return long(unix_ts)
    #Can be applied to complete array
    @classmethod
    def get_vectorize_unixts(cls):
        return np.vectorize(cls.get_unixtimestamp)

    #Gets multiplier c for PI REF: https://otexts.com/fpp2/prediction-intervals.html
    @classmethod
    def compute_PI_multiplier(self, conf_interval=0.95):
        return ndtri((1+conf_interval)/2)
    #Computes column averages
    @classmethod
    def average_listoflists(cls,listoflist):
        return [sum(subl) / len(subl) for subl in zip(*listoflist)]

    @classmethod
    def compute_score_from_interval(cls,prediction_interval,ground_truth,conf_interval=0.95):
        '''
        :param prediction_interval: array of prediction interval with [low,high]
        :param ground_truth: ground truth value
        :return: unscaled score computed from prediction intervals
        score = |GT-Mean|/sigma
        '''
        if any(np.isinf(prediction_interval)):
            return 0# larage bounds I don't know for training time

        if not isinstance(prediction_interval,np.ndarray):
            prediction_interval = np.asarray(prediction_interval)

        if len(prediction_interval) != 2:
            raise ValueError('Prediction Interval array should be lenght 2, provided prediction_interval=',prediction_interval)
        mean = prediction_interval.mean()
        # print('mean', mean,prediction_interval )
        # print('compute score input', prediction_interval,ground_truth)
        if np.isnan(mean):
            mean = 0
            # logger.warning('PointwiseBounded: Mean of Prediction Intervals is NAN!!!!!')

        diff = np.abs(prediction_interval[-1] - mean)
        c = cls.compute_PI_multiplier(conf_interval)
        sigma = diff/c
        score = 0
        # print("sigma",sigma,' mean=',mean,'c=',c)
        if sigma == 0 and np.abs(mean - ground_truth)!=0: #ground truth is not mean value
            score = WatForeADUtils.MAX_ANOMALY_SCORE
            return score

        if sigma == 0 and np.abs(mean - ground_truth)==0: #ground truth is not mean value
            return score

        if not np.isnan(sigma):
            score = np.abs(ground_truth - mean)/sigma
        # print("sigma", sigma, ' mean=', mean, 'c=', c, 'score', score)
        return score


    @classmethod
    def get_models_copy(cls,model, verbose=False):
        if model is None :
            logger.error('No model defined')
            return None

        if isinstance(model,list):
            cp_list = []
            for m in model:
                cp_list.append(pickle.loads(pickle.dumps(m)))
            return cp_list
        else:
            try:
                return pickle.loads(pickle.dumps(model))
            except:
                logger.error('Model Copy failed')
                return None


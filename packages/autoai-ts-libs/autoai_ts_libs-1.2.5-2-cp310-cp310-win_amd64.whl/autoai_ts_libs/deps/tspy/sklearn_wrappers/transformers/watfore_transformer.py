# ************* Begin Copyright - Do not add comments here **************
#   Licensed Materials - Property of IBM
#,
#   (C) Copyright IBM Corp. 2019, 2022, All Rights Reserved
#
# The source code for this program is not published or other-
# wise divested of its trade secrets, irrespective of what has
# been deposited with the U.S. Copyright Office.
# **************************** End Copyright ***************************

"""
@author: Syed Yousaf Shah (syshah@us.ibm.com)

This is a wrapper for watfore to access transforms using autoai api
"""


import numpy as np
#from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
#from autoai_api.autoai import AutoAIEstimator,AutoAITransformer
from sklearn.base import TransformerMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel('WARNING')

try:
    # import autoai_ts_libs.deps.tspy
    import autoai_ts_libs.deps.tspy
    from autoai_ts_libs.deps.tspy.functions import interpolators as tspy_interpolators
    from autoai_ts_libs.deps.tspy.functions import transformers as autoai_ts_libs.deps.tspy_transformers

except Exception as e:
    logger.warning ("Exception importing autoai_ts_libs.deps.tspy")
    logger.warning (e)


class WatForeTransformer(TransformerMixin):

    """
    Forecaster using WatFore library. This class is custom estimator for watfore forecasting models exposing
    watfore forecasters via fit/transform methods

  Parameters
  ----------
  transform_name : str, default='awgn_noise'.
    For ease of use algorithm can be chosen from watfore.Transforms.*
    Transformation that is used to applied from watfore library. Currently available(and growing) transforms are
    'difference','fill_na','shift','awgn_noise','mwgn_noise','z_score'


  default_value: float, default=0
   used by fill_na fills null values with default_value e.g., 0
   Also used by shift transformer, to replace top or bottom shifted values as they move up or down. For shift the
   default=null
  shift_amount: int, default =1
    used by shift transform to tell transformer to shift values by how many timestamps, this could be negative as well
    e.g., -1.

  stdev: float, default = None
    Used by awgn_noise and tells the stdev for noise
  mean: float, default = None
    mean used for both noise models mwgn_noise & awgn_noise.


  append_tranform: bool, default=True.
    When set to True applies transformation on the last column and appends all
    original columns to the right of the transformed column. So output will have columns in order,
    input:
    timestamp, col_a
    output
    timestamp, transformed_col_a, col_a
    input:
    timestamp, col_a, col_b
    output
    timestamp, transformed_col_b, col_a, col_b

    If append_tranform is set to False, on transformed column along with timestamp will be returned and original columns
    will be dropped.
    input:
    timestamp, col_a
    output
    timestamp, transformed_col_a

  ts_icol_loc : array [int], default= -1
    This parameter tells the transformerthe absolute location of the timestamp column. For specifying
     time stamp location put value in array e.g., [0] if 0th column is time stamp. The array is to support
     multiple timestamps in future. If ts_icol_loc = -1 that means no timestamp is provided and all data is
     time series. With ts_icol_loc=-1, the model will assume all the data is ordered and equally sampled.

  ts_ocol_loc: int, default = -1
    This parameter tells the transformer the absolute location of the timestamp column location in the output of the
    transformer, if set to -1 then timestamp will not be includeded otherwise it will be included on specified column
    number. if ts_ocol_loc is specified outside range i.e., < 0 or > 'total number of columns' then timestamp is
    appended at 0 i.e., the first column in the output of the transformer.
    """
    # try:
    #     import os
    #     os.environ['TMP_DIR'] = '../libs/tmp'
    #     os.environ['TS_HOME'] = "../libs/time-series-assembly-1.0.0-jar-with-dependencies.jar"
    # except Exception as e:
    #     logger.error(e)


    def __init__(self, transform_name ='awgn_noise', append_tranform=True,ts_icol_loc=-1,ts_ocol_loc=-1, **kwargs):

         #This will be not be needed once new version of autoai_ts_libs.deps.tspy is released
        # try:
        #      import os
        #      os.environ['TS_HOME'] = os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__)
        #                                                                                     , '../utils'),
        #                                                                        'watfore_javalibs'),
        #                                                           'time-series-assembly-1.0.0-jar-with-dependencies.jar'))
        # except Exception as e:
        #      logger.warning('Unable to set TS_HOME ENV')
        #      logger.error(e)

        self.transform_name = transform_name
        #self.wfts_context = None #wfts_context #context if already open.
        # If true new column with transformed is appended along with original values in transform return value
        self.append_tranform = append_tranform
        self.ts_icol_loc = ts_icol_loc
        self.ts_ocol_loc = ts_ocol_loc
        #try:
        #    wfts_context.stop()
        #except:
         #   print('dd')

        self.debug = False
        if 'debug' in kwargs:
            self.debug = kwargs['debug']

        #if None == self.wfts_context:
        #self.wfts_context = TSContext()

        self.all_args = kwargs
        self.all_args['transform_name'] = self.transform_name
        self.all_args['append_transform'] = self.append_tranform


        #print(ts_icol_loc)
        #print(ts_ocol_loc)
        #self.all_args['algorithm'] = self.algorithm
        self._timeseries = None
        self._timestamps = None
       # self.wfts_context = None



    def get_model_params(self):

       return  self.all_args

    @classmethod
    def get_param_dist(cls, size=None):

        param_dist = {}
        param_dist['transform_name'] = ['difference','fill_na','shift','awgn_noise','mwgn_noise','z_score']

        # These shoule be converted back to ints in fit method
        # doesn't make sense to hpo ithis param_dist['default_value'] = np.arange(0.01, 1, 0.05)
        param_dist['shift_amount'] = np.arange(0.0, 0.15, 0.0001)  # max shift would be 10% of data size
        # Enable later if needed param_dist['stdev'] = np.arange(x, x,x)  #
        # Enable later if needed param_dist['mean'] = np.arange(x, x, x)  #

        return param_dist

    @classmethod
    def get_param_ranges(cls):

        param_ranges = {}
        param_categorical_indices = {}

        param_ranges['transform_name'] = ['difference','fill_na','shift','awgn_noise','mwgn_noise','z_score']
        param_categorical_indices['transform_name'] = (int(0), int(5), int(0))

        param_ranges['shift_amount'] =(float(0), float(0.15), float(0.0001)) # max shift would be 10% of data size

        return param_ranges, param_categorical_indices




    def fit(self, X, y=None):
     #   print('FIT----')
        return self


    def transform(self, X):

        """ A reference implementation of a transform function.
        Parameters
        ----------
        X : {array-like, sparse-matrix}, shape (n_samples, n_features)
            The input samples.
        Returns
        -------
        X_transformed : array, shape (n_samples, n_features)
            The array containing the element-wise square roots of the values
            in ``X``.
        """
        #import traceback
        #import py4j.Py4JError as Py4JError

        #print('In transform')
        # try:
        #     self.wfts_context = autoai_ts_libs.deps.tspy#TSContext(die_on_exit=False)#TSContext()
        # except Exception as e:
        #     print (e)
        #     logger.exception(e)
        #     raise e
        #

        # Input validation
        X = check_array(X, accept_sparse=True,force_all_finite=False) # because X can contain NaN
        # Check that the input is of the same shape as the one passed
        #print('-----------')
        if self.debug:
            print(self.all_args)
            logger.debug(self.all_args)
            logger.debug(str(self.__class__) +' transform \n X=='+str(X))
            print(str(self.__class__) +' transform \n X=='+str(X))

        # This for pipelining with forecaster, the interpolation on timestamp to predict value doesn't make sense
        #Assumes gets [[t]],[[t1],[t2]] shape for predicting values
        #if X.shape[1] == 1:
        #    print('returning the same value')
        #    return X #

        self._timestamps = []
        ts_col = -1
        #Here processes the ts_icol_loc

        if (self.ts_icol_loc == -1):
            #autogenerate ts
            len_ts= X.shape[0]
            for t in range(0,len_ts):
                self._timestamps.append(int(t))
        else:
            #print(self.ts_icol_loc[0])
            ts_col = self.ts_icol_loc[0] # Assuming for now only one timestamp
            if ts_col < 0 or ts_col >= X.shape[1]:
                #self.stop_context()
                #raise RuntimeError(Messages.get_message(str(ts_col), message_id='AUTOAITS0029E'))
                 raise RuntimeError("Improper timestamp column(<0 or >#featurs) for input data. Input timestamp col={0}.")
            #print(X[:,ts_col])
            ts = X[:,ts_col] #X[:, :ts_col+1].flatten()
            #print (ts)
            for t in ts:
                self._timestamps.append(int(t))
             #[X.flatten().tolist()]

        self.n_features_ = X.shape[1] #n_featrues is used later as # of input columns

        #print (X.shape[1])

        #print ( X.shape[1])
        # Check is fit had been called
        ##check_is_fitted(self, 'n_features_')
        #print('-------------')

        # This for pipelining with forecaster, the interpolation on timestamp to predict value doesn't make sense
        #Assumes gets [[t]],[[t1],[t2]] shape for predicting values
        ##if X.shape[1] == 1: return X #

        #print(X.shape[1])
        #print(X[:, 1:])
        #new one's. We need to preserve original columns and add new one's as transformations are applied in chain.

        # For passing through original columns
        all_passthrough_cols = None
        all_transformed_cols = None
        if self.append_tranform:
            all_passthrough_cols = pd.DataFrame(X)
            if ts_col != -1:
                #print(ts_col)
                # Remove ts col, ts_ocol_loc is used to specify location of ts in output
                all_passthrough_cols.drop(columns=[ts_col],inplace=True)



        #For only on ts column, rest of the columns are values so iteratively do the transform on all.
        #Enable parallelizm by making more than 1 threads.
        # Assuming last value column is to apply transformation

        #print(self._timestamps)
        ##if len(X) != self.n_features_: #this check is not needed but leaving in there
         ##   print (len(X))
          ##  print(self.n_features_)
          ##  raise ValueError('Shape of input is different from what was seen'
          ##                   'in `fit`')
        #vals_df_array=[]
        append_ind = 0
        if self.append_tranform:
            total_df_cols = all_passthrough_cols.shape[1]
        for val_ind in range(0, self.n_features_):
            if val_ind != ts_col:
                data_dic = {'timestamp': self._timestamps, 'value': X[:,val_ind]}
                dataframe = pd.DataFrame(data_dic, columns=['timestamp', 'value'])
                dataframe = dataframe.astype(dtype= {"timestamp":"int64","value":"float64"})

                #vals_df_array.append(dataframe)


       # if self.debug:
        #    print(str(self.__class__) +' transform \n Dataframe=='+str(vals_df_array))
         #   print(vals_df_array[0].dtypes)

        #dataframe.replace(np.nan, None, inplace=True)# .fillna('None', inplace=True) # Temp fix for bug in autoai_ts_libs.deps.tspy
        #transformed_array = []

        #for in_df in vals_df_array:
                #print (dataframe)
                trans_x = self._transform(ts_val_df=dataframe).to_df()
                # Handle multiple columns

                # special case for difference operator because it's returned df doesn't have value for first ts
                if self.all_args['transform_name'] == 'difference':

                    #print(append_ind)
                    frist_row = pd.DataFrame({'timestamp': self._timestamps[0], 'value': dataframe['value'].values[0]}, index=[0])
                    trans_x = pd.concat([frist_row, trans_x]).reset_index(drop=True)

                if (all_transformed_cols is None and self.append_tranform == False):
                        all_transformed_cols = pd.DataFrame()
                        all_transformed_cols.insert(append_ind, 'tran_' + str(val_ind),
                                                    trans_x['value'].ravel())
                        append_ind += 1
                    #print(trans_x)
                else:

                    if self.append_tranform:
                        all_passthrough_cols.insert(total_df_cols+append_ind,
                                             'tran_'+str(val_ind), trans_x['value'].ravel())
                    else:

                        all_transformed_cols.insert(append_ind, 'tran_'+str(val_ind), trans_x['value'].ravel())
                    append_ind += 1


        if self.append_tranform:
            #print(all_passthrough_cols.shape[1])
            #trans_x.insert(1, 'original_value', X)
            #all_passthrough_cols.insert(1, 'transformation', trans_x['value'].ravel())  # insert after time stamp column

            #self.stop_context()

            if (self.ts_ocol_loc == -1):
                return all_passthrough_cols.to_numpy()
            else:
                ts_ocol = self.ts_ocol_loc[0]# Assumes one
                if (ts_ocol < 0) or (ts_ocol > all_passthrough_cols.shape[1]):
                    print('Timestamp output location is outside range ts_ocol_loc='+ str(ts_ocol)) # TODO put it in some warning
                    logger.warning('Timestamp output location is outside range ts_ocol_loc='+ str(ts_ocol))
                    all_passthrough_cols.insert(0, 'timestamp', self._timestamps)
                    #raise
                else:
                    all_passthrough_cols.insert(ts_ocol, 'timestamp', self._timestamps)
            return all_passthrough_cols.to_numpy()
        else:

            #print(all_transformed_cols.shape[1])
            #self.stop_context()
            # Here processes the ts_ocol_loc before returning
            if (self.ts_ocol_loc == -1):
                return all_transformed_cols.to_numpy()
            else:
                ts_ocol = self.ts_ocol_loc[0]
                if ts_ocol < 0 or ts_ocol > all_transformed_cols.shape[1]:
                    print('Timestamp output location is outside range ts_ocol_loc='+ str(ts_ocol)) # TODO put it in some warning
                    logger.warning('Timestamp output location is outside range ts_ocol_loc='+ str(ts_ocol))
                    all_transformed_cols.insert(0, 'timestamp', self._timestamps)
                    #raise
                else:
                    all_transformed_cols.insert(ts_ocol, 'timestamp', self._timestamps)

            return all_transformed_cols.to_numpy()#trans_x.to_df()['value'].tolist()

    def _transform(self,ts_val_df,gateway_context=None):

        self._timeseries = autoai_ts_libs.deps.tspy.time_series(ts_val_df, ts_column="timestamp", value_column="value") #autoai_ts_libs.deps.tspy.time_series.df(ts_val_df, "timestamp", "value")

        if self.debug:
            logger.debug(str(self.__class__) + ' transform \n TimeSeries==')
            print(str(self.__class__) + ' transform \n TimeSeries==')
            #self._timeseries.print()

        if self.debug:
            logger.debug(str(self.__class__) + ' transform \n ==' + self.all_args['transform_name'])
            print(str(self.__class__) + ' transform \n ==' + self.all_args['transform_name'])
            #print(self._timeseries)

        if self.all_args['transform_name'] == 'fill_na':
            if 'default_value' not in self.all_args:
                self.all_args['default_value'] = 0
            return self._timeseries.fillna(tspy_interpolators.fill(self.all_args['default_value']))

        if self.all_args['transform_name'] == 'shift':
            #print (self._timeseries)
            #return self._timeseries.shift(1,default_value = 1)

             if 'shift_amount' not in self.all_args:
                 self.all_args['shift_amount'] = 1
             else:
                 if float(self.all_args['shift_amount']) < 1: # coming from AutoAI HPO
                     self.all_args['shift_amount'] = int(len(self._timestamps)* float(self.all_args['shift_amount']))


            #
             if 'default_value' not in self.all_args:
                return self._timeseries.shift(shift_amount = self.all_args['shift_amount'],default_value = 0)
             else:
                return self._timeseries.shift(shift_amount= self.all_args['shift_amount'],
                                               default_value=self.all_args['default_value'])

        if self.all_args['transform_name'] == 'awgn_noise':

            if 'mean' not in self.all_args and 'stdev' not in self.all_args:
                return self._timeseries.transform(autoai_ts_libs.deps.tspy_transformers.awgn())

            if 'mean' in self.all_args and 'stdev' in self.all_args:
                return self._timeseries.transform(
                    autoai_ts_libs.deps.tspy_transformers.awgn(mean=float(self.all_args['mean']),
                                                           sd=float(self.all_args['stdev'])))
            if 'stdev' in self.all_args:
                return self._timeseries.transform(
                    autoai_ts_libs.deps.tspy_transformers.awgn(sd=float(self.all_args['stdev'])))

            if 'mean' in self.all_args:
                return self._timeseries.transform(
                    autoai_ts_libs.deps.tspy_transformers.awgn(mean=float(self.all_args['mean'])))

        if self.all_args['transform_name'] == 'mwgn_noise':
            #if 'mean' not in self.all_args:
            return self._timeseries.transform(autoai_ts_libs.deps.tspy_transformers.mwgn())
            #else:
             #   return self._timeseries.transform(autoai_ts_libs.deps.tspy_transformers.mwgn
             #                                     (mean=float(self.all_args['mean'])))

        if self.all_args['transform_name'] == 'difference':
            return self._timeseries.transform(autoai_ts_libs.deps.tspy_transformers.difference())

        if self.all_args['transform_name'] == 'z_score':
            return self._timeseries.transform(autoai_ts_libs.deps.tspy_transformers.z_score())

        raise ValueError("Invalid 'transform_name' {0} specified.")
        # raise ValueError(Messages.get_message(str(self.all_args['transform_name']), message_id='AUTOAITS0073E'))

    #not needed in new autoai_ts_libs.deps.tspy Ja2020
    # def stop_context(self):
    #     if None != self.wfts_context:
    #         self.wfts_context.stop()


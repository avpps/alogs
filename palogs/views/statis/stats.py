''' Contain functions calculating various statistics from input DataFrame


'''

import pandas as pd
import numpy as np


def prepare_output(*args):
    ''' Split DataFrame to dict with key named:
    ['x', 'x_labels', 'y_1', 'y_..', ...].
    Dict values consit of DataFrame columns values

    '''

    output = {}
    for arg in args:
        output['x_labels'] = arg.index
        arg_m = arg.reset_index(drop=True)
        output['x'] = arg_m.index
        counter = 0
        for i in arg_m.columns:
            output[i] = arg_m[i].values
            counter += 1
    return output


class BaseDf:

    def __init__(self, logs_df):
        self.logs_df = logs_df


class BasicIp(BaseDf):
    ''' Allowed time period frequences at:
    https://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

    '''

    def unique_logs_per_freq(logs_df, frequency='D'):
        ''' Return pandas series with unique logs with time period in defined frequency
        '''

        output = pd.DataFrame(logs_df['log_ip'].resample(frequency).size())
        output['mean'] = output['log_ip'].apply(lambda x: np.mean(output['log_ip']))

        return prepare_output(output)


    def unique_ip_per_freq(logs_df, frequency='D'):
        ''' Return pandas series with unique IP with time period in defined frequency
        '''

        output = logs_df['log_ip'].resample(frequency).apply(lambda x: np.unique(x).shape[0])
        output['mean'] = output['log_ip'].apply(lambda x: np.mean(output['log_ip']))

        return prepare_output(output)


    def ip_freq(logs_df, ip_quantity=15):
        ''' Return pandas series of unique IP frequency
        '''

        output = logs_df.groupby('log_ip').size().sort_values(ascending=False)
        output['mean'] = output['log_ip'].apply(lambda x: np.mean(output['log_ip']))

        return prepare_output(output.head(ip_quantity))
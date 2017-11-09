''' Functions to generate matplotlib charts


'''


import pandas as pd
import matplotlib.pyplot as plt


def one_variable(**kwargs):

    if isinstance(kwargs['x_labels'], pd.core.indexes.datetimes.DatetimeIndex):
        x = kwargs['x_labels']
    else:
        x = kwargs['x']
        x_labels = kwargs['x_labels']
        plt.xticks(x, x_labels)

    del kwargs['x']

    for key, value in kwargs.items():
        if not key.startswith('x_'):
            plt.plot(x, value, label=key)
    
    
    plt.legend()
    plt.show()
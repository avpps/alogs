from django.shortcuts import render
from django.http import Http404

from pandas import DataFrame

from . import prepro
from . import statis

from .statis import stats as sts
from .statis import plots as stp


def home(request):
    return render(request, 'palogs/home.html')

def prepare_logs(request):
    # try to create pandas DataFrame for further use:
    logs_df = prepro.__main__.create_logs_df()

    if isinstance(logs_df, DataFrame):
        pass
    else:
        raise Http404


def create_chart(request):

    #stp.one_variable(**sts.unique_logs_per_freq(logs_df))
    #stp.one_variable(**sts.unique_ip_per_freq(logs_df))
    #stp.one_variable(**sts.ip_freq(logs_df))
    
    return render(request, 'simulator/home.html')
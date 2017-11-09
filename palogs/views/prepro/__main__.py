import pandas as pd
import re


def create_logs_df(file_dir='C:\\repositories\\files\\pa_logs.txt'):
    '''Function create pandas DataFrame with logs details 
    from txt file downloaded from pythonanywhere.

    '''
    
    try:
        with open(file_dir) as logs_file:
            logs_df = pd.DataFrame([])
            for log_line in logs_file:
                extracted_log = list_dict_values(extract_log(log_line))
                extracted_log_df = pd.DataFrame.from_dict(extracted_log)
                logs_df = logs_df.append(extracted_log_df)
    except FileNotFoundError:
        return 'no logs.txt file in {}'.format(file_dir)

    # Turn string column to datetime format:
    logs_df['log_date'] = logs_df['log_date'].apply(
        lambda x: x.replace(':', ' ', 1)).apply(
            lambda x: pd.to_datetime(x))

    logs_df.set_index(['log_date'], inplace=True)

    return logs_df


def list_dict_values(dict):
    '''Turn each input dictionary value into list with this value,
    because pandas 'DataFrame.from_dict' function demand such convention.

    '''
    for key, value in dict.items():
        dict[key] = [value]
    return dict


def extract_log(log):
    ''' Split log string to dictionary for further use in pd.DataFrame

    '''
    
    re_list = {
        'log_ip': r'^[0-9.]*[0-9]',
        'log_date': r'\[.*\]',
        'free_num': r'\s[0-9]*\s[0-9]*\s',
        'other': r'.*',
        'empty': r'\s|'}

    # Initial rough split:
    log_split_1 = []
    for i in re.split('"', log):
        log_split_1.append(i)

    # More detailed spliting with saving to dict:

    ## First item contain always IP and date:
    log_split_2 = {}
    log_split_2['log_ip'] = re.search(
        re_list['log_ip'], log_split_1[0])[0]
    log_split_2['log_date'] = re.search(
        re_list['log_date'], log_split_1[0])[0][1:-1]

    ## Lookfor for other re_list values in others items in log_split_1:
    count = 0
    check_free_num = True
    for i in log_split_1[1:]:
        if check_free_num:
            try:
                log_split_2['free_num'] = re.search(
                    re_list['free_num'], i)[0]
                check = False
            except TypeError:
                continue
            except KeyError:
                pass
        if not bool(re.fullmatch(re_list['empty'], i)):
            try:
                log_split_2['other_{}'.format(count)] = re.search(
                    re_list['other'], i)[0]
                count += 1
            except KeyError:
                pass
    return(log_split_2)

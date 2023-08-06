import pandas as pd
from datetime import datetime

def set_datetime(df):
    """
    Takes in a DataFrame and creates year, month, and day columns for later use. Drops any existing only to avoid any key errors or copy warnings.

    Args:
        df (_DataFrame_): _The DataFrame which has a "date" column and a column which holds data to be replace._

    Returns:
        df _DataFrame_: _The original DataFrame with new year, month, and day columns._
    """
    df = df.drop(['year','month','day'], axis=1, errors='ignore')
    df = df.drop(['Year','Month','Day'], axis=1, errors='ignore')
    df = df.drop(['YEAR','MONTH','DAY'], axis=1, errors='ignore')

    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df.set_index('date',inplace=True)
        
    except:
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df.set_index('date',inplace=True)

    return df
    
def make_testing(df, start_date, end_date, to_replace):
    """
    Creates a temporary DataFrame which will hold information to fill in the permanent DataFrame.

    Args:
        df (_DataFrame_): _A DataFrame which has a 'date' column in datetime format and a column which has data that will be used in filling in missing data._
        start_date (_string_): _A date string for the start of the data that needs to be replaced._
        end_date (_string_): _A date string for the end of the data that needs to be replaced._
        to_replace (_DataFrame_): _A temporary DataFrame which will hold the data used to create values to fill in missing or incorrect data._

    Returns:
        _DataFrame_: _A temporary DataFrame that will be used to fill in missing data._
    """
    start_time = datetime.strptime(start_date, '%Y-%m-%d')
    end_time = datetime.strptime(end_date, '%Y-%m-%d')

    start_year = start_time.year - 5
    end_year = end_time.year + 6
    
    start_day =  start_time.day
    start_month = start_time.month

    end_day = end_time.day
    end_month = end_time.month

    year_diff = end_time.year - start_time.year
    
    testing_data = []

    for year in range(start_year, end_year):
        between_dates = (df
                .loc[f'{year}-{start_month}-{start_day}':f'{year+year_diff}-{end_month}-{end_day}'])
        testing_data.append(between_dates)

    testing_df = pd.concat(testing_data)
    testing_df = testing_df[~testing_df.index.duplicated(keep='first')]
    testing_df.drop(labels=to_replace.index, inplace=True)
    testing_df['month_day'] = (testing_df['month']).astype(str) + "_" + (testing_df['day']).astype(str)
        
    return testing_df
    
def fill_data(df, column, start_date, end_date):
    """
    Takes in a DataFrame, column to fill (str), and two date strings in 'YYYY-mm-dd' format and returns the column filled with data which is the average of the decade that surrounds the chosen dates. 
    
    DataFrame must contain a column labelled 'date' (CASE SENSITIVE). Regardless of format, the dates within the 'date' column should be listed in year,month,day order i.e.:
    
    YYYYmmdd, YYYY/mm/dd, YYYY-mm-dd or any matching order regardless of separator.


    Args:
        df (_DataFrame_): _A DataFrame with a column labelled exactly 'date' with Datetime information and a column that you wish to replace._
        column (_string_): _The name of the column that you wish to be filled._
        start_date (_string_): _The beginning of the dates that you wish to replace. YYYY-mm-dd format._
        end_date (_string_): _The ending of the dates that you wish to replace. YYYY-mm-dd format._

    Returns:
        _DataFrame_: _The original DataFrame with new year, month, and day columns as well as filled in data in the Date range specified._
    """
    
    df = set_datetime(df)
    
    to_replace = df.loc[start_date:end_date].copy()
    
    testing_df = make_testing(df, start_date, end_date, to_replace)
    
    to_replace['month_day'] = (to_replace['month']).astype(str) + "_" + (to_replace['day']).astype(str)
    
    gb = testing_df.groupby(['month_day'])[column].mean().reset_index()

    month_day = gb['month_day'].values
    mean_temp_new = gb[column].values.round(1)
    dict_missing = dict(zip(month_day, mean_temp_new))

    to_replace[column] = to_replace["month_day"].apply(lambda x: dict_missing.get(x))

    df = pd.concat([df, to_replace], axis=0)
    df = df[~df.index.duplicated(keep='last')]
    df = df.drop('month_day', axis=1)
    df = df.sort_index()
    
    return df

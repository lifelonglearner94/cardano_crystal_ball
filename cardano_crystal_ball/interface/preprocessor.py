"""
read dataframe from preprocessor_trends_fg
read dataframe from preprocessor_live_coin_data

"""

import pandas as pd

from cardano_crystal_ball.interface.preprocessing_trends_fg import preprocess_fear_greed, preprocess_trends
from cardano_crystal_ball.interface.preprocessor_live_coin_data import get_data_from_api_and_add_date_related_fields, do_scaling_df_with_live_coin_data
from cardano_crystal_ball.helper.file_system_helper import search_upwards


def check_shape(df_fg, df_trends, df_coin):
    return ((df_fg.shape[0] == df_trends.shape[0]) and \
        (df_fg.shape[0] >= df_coin.shape[0]) and \
        (df_trends.shape[0] >= df_coin.shape[0]))

def check_datatypes(df):
    import ipdb; ipdb.set_trace()
    return True

def preprocessor(start=None, end=None, csv_fg=None, csv_trends=None):

    """
    start, end  - must be a python datetime. the cardano coin data is fetched via live_coin_watch

    csv_fg - path to the csv file with the fear&Greed values
    csv_trend  - path to the csv file with the google trend data
    """

    if end == None :
        end = pd.Timestamp.today(tz='UTC')
    if start == None :
        start = end - pd.Timedelta(days=5)

    if csv_fg == None :
        csv_fg = search_upwards('raw_data')/'raw_data/Fear_and_greed_index_5Y.csv'
    if csv_trends == None :
        csv_trends = search_upwards('raw_data')/'raw_data/trends.csv'

    df_trends = preprocess_trends(csv_trends)
    df_fg = preprocess_fear_greed(csv_fg)


    df_temp = get_data_from_api_and_add_date_related_fields(int(start.timestamp()),int(end.timestamp()))
    df_coin = do_scaling_df_with_live_coin_data(df_temp)

    df_coin = df_coin.set_index('date')
    df_coin.index = pd.to_datetime(df_coin.index)

    new_df = df_fg[df_fg.index >= df_coin.index.min()]
    temp_fg = new_df[new_df.index <= df_coin.index.max()]

    new_trends = df_trends[df_trends.index >= df_coin.index.min()]
    temp_trends = new_trends[new_trends.index <= df_coin.index.max()]

    # check Datatypes of the three dataframes
    for df in [temp_fg, temp_trends, df_coin]:
        if not check_datatypes(df):
            raise ValueError(f"The datatype of the dataframe with the columns: {df.columns} is not correct")

    # check if the three dataframes have the right(same) shape
    if not check_shape(temp_fg, temp_trends, df_coin):
        raise ValueError(f"The shape of the three dataframes df_fg {temp_fg.shape}, df_coin  {df_coin.shape} and df_trends {temp_trends.shape} is not correct!\nPreprocessing aborted!")

    print (df_coin.dytpes)
    print (df_coin.dytpes)
    print (df_coin.dytpes)


    df = pd.concat([df_coin, temp_fg, temp_trends], axis=1)

    df.to_csv (search_upwards('raw_data')/'raw_data/preprocess.csv')

    return df

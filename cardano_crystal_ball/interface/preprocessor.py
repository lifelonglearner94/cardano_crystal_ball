"""
read dataframe from preprocessor_trends_fg
read dataframe from preprocessor_live_coin_data

"""

import pandas as pd

from preprocessing_trends_fg import preprocess_fear_greed, preprocess_trends
from preprocessor_live_coin_data import get_data_from_api_and_add_date_related_fields

def preprocessor(start, end, csv_fg, csv_trends):

    """
    start, end  - must be a python datetime. the cardano coin data is fetched via live_coin_watch
    csv_fg - path to the csv file with the fear&Greed values
    csv_trend  - path to the csv file with the google trend data
    """

    df_trends = preprocess_trends(csv_trends)
    df_fg = preprocess_fear_greed(csv_fg)


    df_coin = get_data_from_api_and_add_date_related_fields(int(start.timestamp()),int(end.timestamp()))
    df_coin = df_coin.set_index('date')
    df_coin.index = pd.to_datetime(df_coin.index)

    new_df = df_fg[df_fg.index >= df_coin['date'].min()]
    temp_fg = new_df[new_df.index <= df_coin['date'].max()]

    df_trends = preprocess_trends(csv_trends)
    new_trends = df_trends[df_trends.index >= df_coin['date'].min()]
    temp_trends = new_trends[new_trends.index <= df_coin['date'].max()]

    df = pd.concat([df_coin, temp_fg, temp_trends], axis=1)

    df.to_csv ('raw_data/preprocess.csv')

    return df

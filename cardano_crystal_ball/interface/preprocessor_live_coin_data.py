import pandas as pd

from apis.live_coin_watch.utils import api_request, get_alot_of_data, convert_timestamp_to_time_string

from sklearn.preprocessing import MinMaxScaler



def get_data_from_api_and_add_date_related_fields (start, end):
    """

    - read data from live_coin_watch via utils.py
    - add columns for year, week, weekday and hour to the dataframe

    returns a dataframe with the added columns

    """

    start_as_string = convert_timestamp_to_time_string(start, False)
    end_as_string = convert_timestamp_to_time_string(end, False)

    df = get_alot_of_data(start_as_string, end_as_string)

    # extract year, week and weekday from timestamp in new fields
    # df_add_fields = pd.to_datetime(df['date']).dt.isocalendar()
    # df[df_add_fields.columns] = df_add_fields

    # extract hour and put it into a new field
    # df_hour = pd.to_datetime(df['date']).dt.hour
    # df['hour'] = df_hour

    return df


def do_scaling_df_with_live_coin_data (df, columns=["volume", "cap", "liquidity"] ):
    """
    all values in the columns of the columns listshould will be be scaled with MinMaxScaler
    """
    scaler = MinMaxScaler()
    # scale only this columns
    # columns=["volume", "cap", "liquidity"]
    df[columns] = scaler.fit_transform(df[columns])
    return df

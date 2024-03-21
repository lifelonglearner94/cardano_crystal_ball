import pytest
import pandas as pd

from interface.preprocessor_live_coin_data import get_data_from_api_and_add_date_related_fields, do_scaling_df_with_live_coin_data


def test_processor_franz():
    start = pd.Timestamp(year=2024,month=1, day=1)
    end = pd.Timestamp(year=2024,month=2, day=1)
    df = get_data_from_api_and_add_date_related_fields(int(start.timestamp()),int(end.timestamp()))
    assert(len(df)>10)
    assert(len(df.columns) == 5)

def test_do_scaling_df_with_live_coin_data():
    start = pd.Timestamp(year=2024,month=1, day=1)
    end = pd.Timestamp(year=2024,month=1, day=3)
    df = get_data_from_api_and_add_date_related_fields(int(start.timestamp()),int(end.timestamp()))

    columns=["volume", "cap"]
    df1 = do_scaling_df_with_live_coin_data(df,columns)
    assert df1['liquidity'].max() > 10
    assert df1['cap'].max() <= 1
    assert df1['volume'].max() <= 1
    assert df1['rate'].max() <= 1

import pytest
import pandas as pd

from cardano_crystal_ball.interface.preprocessor_live_coin_data import get_data_from_api_and_add_date_related_fields


def test_processor_franz():
    start = pd.Timestamp(year=2024,month=1, day=1)
    end = pd.Timestamp(year=2024,month=2, day=1)
    df = get_data_from_api_and_add_date_related_fields(int(start.timestamp()),int(end.timestamp()))
    assert(len(df)>10)
    assert(len(df.columns) == 5)

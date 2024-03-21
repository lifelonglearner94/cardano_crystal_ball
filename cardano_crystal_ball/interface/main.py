# from cardano_crystal_ball.apis.live_coin_watch.utils import get_api_limit, api_request, get_4_days_of_data, get_alot_of_data
# from cardano_crystal_ball.interface.preprocessor_live_coin_data import  get_data_from_api_and_add_date_related_fields
from preprocessor import    preprocessor
import pandas as pd
from cardano_crystal_ball.helper.file_system_helper import search_upwards


if __name__ == '__main__':

    start = pd.Timestamp(year=2023,month=1, day=1)
    end = pd.Timestamp(year=2023,month=1, day=3)
    csv_fg= search_upwards('raw_data')/'raw_data/Fear_and_greed_index_5Y.csv'
    csv_trend= search_upwards('raw_data')/'raw_data/trends.csv'
    df = preprocessor(start, end, csv_fg, csv_trend)
    # response = api_request(int(start.timestamp()), int(end.timestamp()))
    # response = api_request(int(start.timestamp()), int(end.timestamp()))

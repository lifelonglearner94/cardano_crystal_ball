import pandas as pd
from cardano_crystal_ball.params import *
from cardano_crystal_ball.apis.live_coin_watch.load_more_data import *
from cardano_crystal_ball.apis.fg.get_fg import *
from cardano_crystal_ball.apis.google_trends.get_trends import *
from pandas.api.types import is_numeric_dtype
from cardano_crystal_ball.interface.preprocessor_live_coin_data import *
#from cardano_crystal_ball.interface.preprocessing_trends_fg import *
import glob
from datetime import datetime
from darts import TimeSeries
from darts import utils



def update_data_until_today() -> pd.DataFrame:

    processed_path = Path(LOCAL_DATA_PATH).joinpath('processed')

    raw_path_0 = Path(LOCAL_DATA_PATH).joinpath('raw')

    if not processed_path.exists():
            os.makedirs(processed_path)

    if not raw_path_0.exists():
        os.makedirs(raw_path_0)


    #getting the newest processed csv file
    csv_files = glob.glob(os.path.join(processed_path, '*.csv'))
    if not csv_files:
        raise FileNotFoundError(f"No File found in the directory: {processed_path}")
    newest_csv = max(csv_files, key=os.path.getctime)

    newest_csv_as_df = pd.read_csv(newest_csv, index_col=0, parse_dates=True)

    #getting first and last date
    first_date = newest_csv_as_df.index.min()
    last_date = newest_csv_as_df.index.max()
    assert first_date.strftime("%Y-%m-%d") == START_DATE

    #getting new livecoin data until now!
    today_date_time = datetime.now()
    now_date_time_str = today_date_time.strftime("%Y-%m-%d %H:%M:%S")
    new_raw_livecoin_data = load_more_livecoin_data_and_save(last_date.strftime("%Y-%m-%d %H:%M:%S"), now_date_time_str)

    #getting new fg data until now
    date1 = datetime(today_date_time.year, today_date_time.month, today_date_time.day)
    date2 = last_date.to_pydatetime()
    difference = date1 - date2
    difference_in_days = difference.days
    new_raw_fg_data = get_fg_from_api(limit=difference_in_days + 3)

    #getting google trends data
    new_raw_trends_data = get_trends(["Bitcoin","Cardano","cardano price","cryptocurrency","Ethereum"])

    #preprocessing
    raw_path = os.path.join(LOCAL_DATA_PATH, 'raw', 'Hourly_ada_utc.csv') #if it does not exist it should fetch new data.
    if os.path.exists(raw_path):
        full_existing_livecoin_data = pd.read_csv(raw_path, index_col=0, parse_dates=True)
        full_existing_livecoin_data_cut = full_existing_livecoin_data[full_existing_livecoin_data.index >= pd.to_datetime(START_DATE)]
        full_raw_livecoin_data = pd.concat([full_existing_livecoin_data_cut, new_raw_livecoin_data], axis=0)
    else:
        full_raw_livecoin_data = load_more_livecoin_data_and_save(START_DATE + " 00:00:00", now_date_time_str, full_data=True)

    full_raw_livecoin_data.drop_duplicates(inplace=True)

    processed_livecoin_data = do_scaling_df_with_live_coin_data(full_raw_livecoin_data)

    processed_fg_data = preprocess_fear_greed(new_raw_fg_data)
    processed_trends_data = preprocess_trends(new_raw_trends_data)

    #concat the preprocessed
    processed_concatinated = pd.concat([processed_livecoin_data, processed_fg_data, processed_trends_data], axis=1)

    #concat the existing data with the new data
    final_concatinated = pd.concat([newest_csv_as_df, processed_concatinated], axis=0)


    final_concatinated = final_concatinated.dropna()

    duplicate_indices = final_concatinated.index.duplicated()
    if any(duplicate_indices):
        final_concatinated = final_concatinated[~duplicate_indices]

    try:
        final_result = final_timeseries_processing(final_concatinated)
    except:
        final_result = final_concatinated

    #save to csv
    full_csv_path = os.path.join(processed_path, f'full_processed_data_from_{START_DATE}_to_{today_date_time.strftime("%Y-%m-%d")}.csv')

    final_result.to_csv(full_csv_path)

    print(f"✅ Updated data succesfully written to {full_csv_path}")

    return final_result


def final_timeseries_processing(df):


    df_ts = TimeSeries.from_dataframe(df, fill_missing_dates=True, freq = 'h')
    df_ts = utils.missing_values.fill_missing_values(df_ts)

    result_df = df_ts.pd_dataframe()

    return result_df


def preprocess_trends(df, kw_list=["Bitcoin","Cardano","cardano price","cryptocurrency","Ethereum",]):


    # Drop duplicates
    df = df.drop_duplicates()

    # Turn dates from string to datetime
    df['Week'] = pd.to_datetime(df['Week'])

    # Add new week at the end, as new end date for later conversion to hourly data.
    new_date = df['Week'].iloc[-1] + pd.Timedelta(days=7)
    new_row = pd.DataFrame({'Week': new_date}, index=[1])
    df = pd.concat([df, new_row])

    # Setting date as index. Turning weekly into hourly data.
    # Replace missing values with the preceding value using forward fill
    df.set_index('Week', inplace=True)
    df_hourly = df.resample('h').ffill()

    # Dropping last row, which was used as end date.
    df_hourly = df_hourly[:-1]

    # Check if all columns are of numeric value for scaling
    for col in df_hourly.columns:
        if is_numeric_dtype(df_hourly[col]) == False:
            df_hourly[col] = pd.to_numeric(df_hourly[col], errors='coerce')
            df_hourly[col] = df_hourly[col].fillna(1)       # NaN gets replace by 1

    # Min_Max Scale data
    df_hourly = df_hourly / 100

    return df_hourly

def preprocess_fear_greed(df):


    # Drop irrelevant columns
    df = df[['value', 'timestamp']]

    # Drop duplicates
    df = df.drop_duplicates()

    # Turn dates from string to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Add new week at the end, as new end date for later conversion to hourly data.
    new_date = df['timestamp'].iloc[-1] + pd.Timedelta(days=1)
    new_row = pd.DataFrame({'timestamp': new_date}, index=[1])
    df = pd.concat([df, new_row])

    # Setting date as index. Turning weekly into hourly data.
    # Replace missing values with the preceding value using forward fill
    df.set_index('timestamp', inplace=True)
    df_hourly = df.resample('h').ffill()

    # Dropping last row, which was used as end date.
    df_hourly = df_hourly[:-1]

    # Check if all columns are of numeric value for scaling
    if is_numeric_dtype(df_hourly['value']) == False:
        df_hourly['value'] = pd.to_numeric(df_hourly['value'], errors='coerce')
        df_hourly['value'] = df_hourly['value'].fillna(1)     # NaN gets replace with 1

    df_hourly.rename(columns={'value': 'fg_value'}, inplace=True)

    # Min_Max Scale data
    df_hourly = df_hourly / 100

    return df_hourly

if __name__ == "__main__":
    df = update_data_until_today()
    print(df)

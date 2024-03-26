import pandas as pd
from pandas.api.types import is_numeric_dtype
from cardano_crystal_ball.apis.fg.get_fg import get_fg_from_api

def preprocess_trends(csv):
    """
    Taking weekly Google Trends data, for search terms
        - Cardano (Topic)
        - Bitcoin (Topic)
        - Cryptocurrency (topic)
        - Ethereum (Topic)
        - Cardano price (search query)
        as a CSV.

        Returns: DataFrame with data converted to hourly and MinMaxScaled.
    """
    # Load Trends data into dataframe
    df = pd.read_csv(csv)

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


def preprocess_fear_greed(csv):
    """
    Takes csv file with daily Fear and Greed data.
    Returns DataFrame with hourly data, and MinMaxScaled.

    """
    # read newest values from api https://api.alternative.me/fng/
    try: # Load Trends data into dataframe
        df = get_fg_from_api(limit="1000")
        if df.shape[0] < 10: # in case of no Data
            df = pd.read_csv(csv)
    except: # if api or internet is not available
        df = pd.read_csv(csv)

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
    df = preprocess_fear_greed(None)
    print (df.shape)
    print(df.info())

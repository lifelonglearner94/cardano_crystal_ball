import pandas as pd
from pandas.api.types import is_numeric_dtype

def preprocess_trends(csv):
    """
    Taking Google Trends data, for search terms
        - Cardano (Topic)
        - Bitcoin (Topic)
        - Cryptocurrency (topic)
        - Ethereum (Topic)
        - Cardano price (search query)
        as a CSV.
        Turn it
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
            df_hourly[col].fillna(1, inplace=True)       # NaN gets replace by 1

    # Min_Max Scale data
    df_hourly = df_hourly / 100

    return df_hourly


def preprocess_fear_greed(csv):
    # Load Trends data into dataframe
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
        df_hourly['value'].fillna(1, inplace=True)     # NaN gets replace with 1

    # Min_Max Scale data
    df_hourly = df_hourly / 100

    return df_hourly

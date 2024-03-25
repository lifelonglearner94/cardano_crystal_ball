from cardano_crystal_ball.interface.main import *
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def get_yesterdays_rate(pred) -> tuple:

    DATA_SOURCE = "local" #remove later, when it is in a env var

    if DATA_SOURCE == "local":

        first_date = pred[0].time_index[0]

        date_minus_24h = first_date - pd.Timedelta(hours=24)

        processed_data_path_basic = Path(LOCAL_DATA_PATH).joinpath('processed')


        csv_files = glob.glob(os.path.join(processed_data_path_basic, '*.csv'))

        if not csv_files:
            return None

        newest_csv = max(csv_files, key=os.path.getctime)

        df = pd.read_csv(newest_csv, index_col=0, parse_dates=True)

        slice_df = df.loc[date_minus_24h:first_date - pd.Timedelta(hours=1), "rate"]

    return slice_df.tolist(), date_minus_24h.strftime('%Y-%m-%d %H:%M:%S')


def upwards_trend(pred) -> bool:

    pred_array = pred.values()

    zero_to_23 = np.arange(len(pred)).reshape(-1, 1)

    model = LinearRegression().fit(zero_to_23, pred_array)

    slope = model.coef_[0][0]

    return True if slope > 0 else False

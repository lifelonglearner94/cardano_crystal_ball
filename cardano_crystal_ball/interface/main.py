import pandas as pd
import numpy as np
import darts
import os

from cardano_crystal_ball.interface.preprocessor import  preprocessor
from cardano_crystal_ball.helper.file_system_helper import search_upwards
from cardano_crystal_ball.ml_logic.model import *
from cardano_crystal_ball.params import *
from darts import TimeSeries
from pathlib import Path
from cardano_crystal_ball.ml_logic.registry import *
from cardano_crystal_ball.ml_logic.data import load_data_to_bq

from pathlib import Path
import glob
from cardano_crystal_ball.data_update.auto_update import update_data_until_today

def preprocess():
    """
    - Check if preprocess.csv is not exist then run preprocess
    """
    try: # this is the new way of merging, preprocessing and updating data
        df = update_data_until_today()
    except: # if the above doesn't work use the old way below

        processed_csv_data_path = Path(LOCAL_DATA_PATH).joinpath('processed','preprocess.csv')

        processed_data_path_basic = Path(LOCAL_DATA_PATH).joinpath('processed')

        if not processed_data_path_basic.exists():
            os.makedirs(processed_data_path_basic)
            start = pd.Timestamp(START_DATE)
            end = pd.Timestamp(year=2024,month=3, day=26)
            csv_fg = Path(LOCAL_DATA_PATH).joinpath(LOCAL_DATA_PATH,'raw','Fear_and_greed_index_5Y.csv')
            csv_trend = Path(LOCAL_DATA_PATH).joinpath(LOCAL_DATA_PATH,'raw','trends.csv')
            df = preprocessor(start, end, csv_fg, csv_trend)
            df.to_csv(processed_csv_data_path)
        else:
            df = pd.read_csv(Path(processed_csv_data_path))


    load_data_to_bq(
        df,
        gcp_project=GCP_PROJECT,
        bq_dataset=BQ_DATASET,
        table=f'processed_{START_DATE}',
        truncate=True
    )
    return df

def initialize_compile_model():
    # try:
    #     model = load_model()
    # except:
    #     model = None

    model = None

    if model is None:

        model = initialize_and_compile_model(
                                    type_of_model = MODEL_TYPE,
                                    )
    return model

def training():
    #everyday auto_update should be called before training !
    model = load_model()

    processed_path = os.path.join(LOCAL_DATA_PATH,'processed')

    #loading the newest, processed full data
    csv_files = glob.glob(os.path.join(processed_path, '*.csv'))
    if not csv_files:
        raise FileNotFoundError(f"No File found in the directory: {processed_path}")
    newest_csv = max(csv_files, key=os.path.getctime)
    print(f"newest_data_name: {newest_csv}")

    df = pd.read_csv(newest_csv, index_col=0, parse_dates=True)

    X = df.drop(columns = ["rate"])
    y = df[["rate"]]


    X_timeseries = TimeSeries.from_dataframe(X,  fill_missing_dates=True, freq = 'h')
    y_timeseries = TimeSeries.from_dataframe(y, fill_missing_dates=True, freq = 'h')


    X_timeseries = darts.utils.missing_values.fill_missing_values(X_timeseries)
    y_timeseries = darts.utils.missing_values.fill_missing_values(y_timeseries)

    X_timeseries = X_timeseries.astype("float32")
    y_timeseries = y_timeseries.astype("float32")

    #X_train, X_test = X_timeseries.split_before(len(X_timeseries)-24) # when the model is in production we should remove these lines
    #y_train, y_test = y_timeseries.split_before(len(y_timeseries)-24) # when the model is in production we should remove these lines

    X_train, X_val = X_timeseries.split_before(0.9)
    y_train, y_val = y_timeseries.split_before(0.9)


    model = train_model(model,
                        MODEL_TYPE,
                        y_train,
                        y_val,
                        X_train,
                        X_val
                        )
    save_model(model)
    return model

def prediction():
    prediction = predict_next_24h()
    return prediction




if __name__ == '__main__':

    try:
        preprocess()
        initialize_compile_model()
        training()
        #retraining()

        prediction = prediction()
        #print ('prediction ------->  ' , prediction)
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)

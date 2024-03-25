from cardano_crystal_ball.interface.preprocessor import  preprocessor
import pandas as pd
from cardano_crystal_ball.helper.file_system_helper import search_upwards
from cardano_crystal_ball.ml_logic.model import *
import darts
from cardano_crystal_ball.params import *
from darts import TimeSeries
import os
from pathlib import Path
from cardano_crystal_ball.ml_logic.registry import *


def preprocess():
    """
    - Check if preprocess.csv is not exist then run preprocess
    """


    processed_data_path = Path(LOCAL_DATA_PATH).joinpath('processed','preprocess.csv')
    if not processed_data_path.exists():
        start = pd.Timestamp(year=2023,month=1, day=1)
        end = pd.Timestamp(year=2023,month=2, day=18)
        csv_fg= search_upwards('raw_data')/'raw_data/Fear_and_greed_index_5Y.csv'
        csv_trend= search_upwards('raw_data')/'raw_data/trends.csv'
        df = preprocessor(start, end, csv_fg, csv_trend)
    else:
        df = pd.read_csv(Path(processed_data_path))

    return df

def initialize_compile_model():
    model = load_model()


    if model is None:

        model = initialize_and_compile_model(
                                    type_of_model = MODEL_TYPE,
                                    start_learning_rate=0.01,
                                    learning_rate_decay=True,
                                    batch_size=32,
                                    epochs=50,
                                    es_patience=7,
                                    accelerator="cpu"
                                    )
    return model

def training():

    model = load_model()
    csv_path = os.path.join(LOCAL_DATA_PATH,'processed', 'preprocess.csv')
    df = pd.read_csv(csv_path)


    X = df.drop(columns = ["rate"])#, "rate_scaled"])
    y = df[['Unnamed: 0', "rate"]]


    X_timeseries = TimeSeries.from_dataframe(X, 'Unnamed: 0', fill_missing_dates=True, freq = 'h')
    y_timeseries = TimeSeries.from_dataframe(y,'Unnamed: 0', fill_missing_dates=True, freq = 'h')


    X_timeseries = darts.utils.missing_values.fill_missing_values(X_timeseries)
    y_timeseries = darts.utils.missing_values.fill_missing_values(y_timeseries)

    X_train, X_test = X_timeseries.split_before(len(X_timeseries)-24)
    y_train, y_test = y_timeseries.split_before(len(y_timeseries)-24)

    X_train, X_val = X_train.split_before(0.7)
    y_train, y_val = y_train.split_before(0.7)


    model = train_model(model,
                        MODEL_TYPE,
                        y_train,
                        y_val,
                        X_train,
                        X_val,
                        future_covariates=None,
                        future_covariates_val=None
                        )
    save_model(model)
    return model

def prediction():
    prediction = predict_next_24h()

    return prediction



if __name__ == '__main__':

    # start = pd.Timestamp(year=2023,month=1, day=1)
    # end = pd.Timestamp(year=2023,month=1, day=3)
    # csv_fg= search_upwards('raw_data')/'raw_data/Fear_and_greed_index_5Y.csv'
    # csv_trend= search_upwards('raw_data')/'raw_data/trends.csv'
    # df = preprocessor(start, end, csv_fg, csv_trend)
    # # response = api_request(int(start.timestamp()), int(end.timestamp()))
    # # response = api_request(int(start.timestamp()), int(end.timestamp()))
    try:
        #preprocess()
        #initialize_compile_model()
        #training()

        prediction = prediction()
        print ('prediction ------->  ' , prediction)
    except:
        import sys
        import traceback

        import ipdb
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)

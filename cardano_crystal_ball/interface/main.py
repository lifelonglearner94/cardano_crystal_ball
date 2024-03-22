# from cardano_crystal_ball.apis.live_coin_watch.utils import get_api_limit, api_request, get_4_days_of_data, get_alot_of_data
# from cardano_crystal_ball.interface.preprocessor_live_coin_data import  get_data_from_api_and_add_date_related_fields
from preprocessor import    preprocessor
import pandas as pd
from cardano_crystal_ball.helper.file_system_helper import search_upwards
from cardano_crystal_ball.ml_logic.model import *
from darts.utils.missing_values import fill_missing_values
from params import *

def workflow():
    """
    Workflow:
        - Initializing the model
        - Compiling the model
        - Training the model
        - Evaluating the model
        - Do prediction

    return:
        - Prediction results
    """
    df = preprocessor(start, end, csv_fg, csv_trend)

    X = df.drop(columns = ["rate"])#, "rate_scaled"])
    y = df[["rate"]]

    X_timeseries = TimeSeries.from_dataframe(X, fill_missing_dates=True, freq="h")
    y_timeseries = TimeSeries.from_dataframe(y, fill_missing_dates=True, freq="h")


    X_timeseries = fill_missing_values(X_timeseries)
    y_timeseries = fill_missing_values(y_timeseries)

    X_train, X_test = X_timeseries.split_before(len(y_timeseries)-24)
    y_train, y_test = y_timeseries.split_before(len(y_timeseries)-24)

    X_train, X_val = X_train.split_before(0.8)
    y_train, y_val = y_train.split_before(0.8)


    model = initialize_and_compile_model(
                                        type_of_model = MODEL_TYPE,
                                        start_learning_rate=0.01,
                                        learning_rate_decay=True,
                                        batch_size=32,
                                        epochs=50,
                                        es_patience=7,
                                        accelerator="cpu"
                                        )


    model = train_model(model,
                        MODEL_TYPE,
                        y_train,
                        y_val,
                        X_train,
                        X_val,
                        future_covariates=None,
                        future_covariates_val=None
                        )

prediction = predict_next_24h()
score = evaluate_model(

)

if __name__ == '__main__':

    start = pd.Timestamp(year=2023,month=1, day=1)
    end = pd.Timestamp(year=2023,month=1, day=3)
    csv_fg= search_upwards('raw_data')/'raw_data/Fear_and_greed_index_5Y.csv'
    csv_trend= search_upwards('raw_data')/'raw_data/trends.csv'
    df = preprocessor(start, end, csv_fg, csv_trend)
    # response = api_request(int(start.timestamp()), int(end.timestamp()))
    # response = api_request(int(start.timestamp()), int(end.timestamp()))

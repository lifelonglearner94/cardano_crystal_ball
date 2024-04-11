from darts.models import BlockRNNModel
from torchmetrics.regression import SymmetricMeanAbsolutePercentageError, MeanAbsoluteError
import torch
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from darts import TimeSeries
from darts.metrics import smape, mae
from cardano_crystal_ball.ml_logic.registry import *
from darts.models.forecasting.tft_model import TFTModel
from darts.utils.likelihood_models import QuantileRegression
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from pytorch_lightning.loggers import CSVLogger

def initialize_and_compile_model(type_of_model: str = 'RNN',
                                 start_learning_rate=0.001,
                                 learning_rate_decay=True,
                                 batch_size=32,
                                 epochs=500,
                                 es_patience=12,
                                 early_stopping = True,
                                 n_rnn_layers = 3,
                                 accelerator="cpu"):

    #for TFT add:   num_attention_heads, lstm_layers, hidden_size   parameters


    my_stopper = EarlyStopping(
                            monitor="val_loss",
                            patience=es_patience,
                            min_delta=0.005,
                            mode='min',
                            )
    if early_stopping:
        pl_trainer_kwargs={"callbacks": [my_stopper],
                        "accelerator": accelerator}
    else:
        pl_trainer_kwargs=None

    if learning_rate_decay:
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau #reduce learning rate when a metric has stopped improving
    else:
        lr_scheduler = None

    if type_of_model == "RNN":
        model = BlockRNNModel(
                            model = "LSTM",
                            input_chunk_length=120,
                            output_chunk_length=24,
                            n_rnn_layers = n_rnn_layers,
                            dropout=0.2,
                            loss_fn=torch.nn.MSELoss(),
                            optimizer_cls = torch.optim.Adam,
                            optimizer_kwargs = {'lr': start_learning_rate}, #learning rate
                            lr_scheduler_cls = lr_scheduler,
                            torch_metrics=SymmetricMeanAbsolutePercentageError(),
                            batch_size = batch_size,
                            pl_trainer_kwargs = pl_trainer_kwargs,
                            n_epochs=epochs
                            )


    elif type_of_model == "TFT":

        # Input is 5 days (in hours), output is 24 hours.
        input_chunk_length = (5*24)
        output_chunk_length = 24

        my_stopper = EarlyStopping(
                    monitor="val_loss",
                    patience=5,
                    min_delta=0.001,
                    mode='min',
                )

        logger = CSVLogger("raw_data/logs", name="TFT_logs")

        pl_trainer_kwargs={"callbacks": [my_stopper],
                           "accelerator": "cpu",
                           "logger": logger}


        model = TFTModel(input_chunk_length =input_chunk_length ,
               output_chunk_length = output_chunk_length,
               pl_trainer_kwargs = pl_trainer_kwargs,
               lstm_layers=1,
               num_attention_heads=8,
               dropout=0.2,
               batch_size=16,
               hidden_size=32,
               torch_metrics=MeanAbsoluteError(),
               n_epochs=1000,
               likelihood=QuantileRegression(),
               lr_scheduler_cls = lr_scheduler,
               random_state=0,
              ) 

    print("✅ Model initialized & compiled")
    save_model(model)
    return model



def train_model(model,
                type_of_model: str,
                y_train: TimeSeries,
                y_val: TimeSeries,
                past_covariates: TimeSeries,
                past_covariates_val: TimeSeries):

    combined_y = y_train.concatenate(y_val)
    combined_past_covariates = past_covariates.concatenate(past_covariates_val)

    model.fit(series=y_train,    # the target training data
        past_covariates=past_covariates,     # the multi covariate features training data
        val_series=y_val,  # the target validation data
        val_past_covariates=past_covariates_val,   # the multi covariate features validation data
        verbose=True)

    n_epochs_model_1 = model.epochs_trained

    model_2 = initialize_and_compile_model("RNN", learning_rate_decay=False, early_stopping=False, epochs=n_epochs_model_1)

    model_2.fit(series=combined_y,    # the target training data
        past_covariates=combined_past_covariates,     # the multi covariate features training data
        verbose=True)

    print(f"✅ RNN Model trained on {combined_y.duration}.")
    save_model(model_2)
    return model_2


def train_tft():

    model = load_model()
    csv_path = os.path.join(LOCAL_DATA_PATH,'processed', 'preprocess.csv')
    df = pd.read_csv(csv_path)

    # Further processing for TFT model.
    df.index = pd.to_datetime(df.index)
    df.interpolate(method='linear', inplace=True)

    target = df['rate_scaled']
    past_cov = df.drop(columns=['rate', 'rate_scaled'])
    future_cov = pd.DataFrame(df.index.to_series().dt.dayofweek)

    future_scaler = MinMaxScaler()
    future_cov = pd.DataFrame(future_scaler.fit_transform(future_cov))

    # Defining train, test, val.
    test = 24
    train = int(0.8*len(df))
    val = len(df) - train -test

    # Splitting data between future and past for train, test and val.
    y_train = target[-train-val-test:-val - test]
    future_cov_train = future_cov[-train-val-test:-val]
    past_cov_train = past_cov[-train-val-test:-val - test]
    y_val = target[-val-test:-test]
    past_cov_val = past_cov[-val-test:-test]
    future_cov_val = future_cov[-val-test:]
    y_test = target[-test:]

    # Transforming the Panda series and dataframes into Darts TimeSeries
    y_train_series = TimeSeries.from_series(y_train)
    past_cov_train_series = TimeSeries.from_dataframe(past_cov_train)
    future_cov_train_series = TimeSeries.from_dataframe(future_cov_train)

    y_val_series = TimeSeries.from_series(y_val)
    past_cov_val_series = TimeSeries.from_dataframe(past_cov_val)
    future_cov_val_series = TimeSeries.from_dataframe(future_cov_val)

    y_test_series = TimeSeries.from_series(y_test)

    # Train model
    model.fit(series=y_train_series,
        past_covariates = past_cov_train_series,
        future_covariates = future_cov_train_series,
        val_series=y_val_series,
        val_past_covariates=past_cov_val_series,
        val_future_covariates=future_cov_val_series,
        verbose=True)

    save_model(model)

    return model


def evaluate_model(true_series: TimeSeries, forecasted_series: TimeSeries) -> float:

    smape_score = smape(true_series, forecasted_series) # maybe change the metric !!

    mae_score = mae(true_series, forecasted_series)

    print(f"✅ Model evaluated, SMAPE: {round(smape_score, 2)} %\n MAE = {mae_score}")

    return smape_score


def predict_next_24h( very_latest_time_series=None, very_latest_past_covariates=None) -> TimeSeries:

    model = load_model()
    prediction_series = model.predict(n=24, series=very_latest_time_series, past_covariates=very_latest_past_covariates) #Predict the n time step following the end of the training series, or of the specified series.

    return prediction_series

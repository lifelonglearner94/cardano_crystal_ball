from darts.models import BlockRNNModel
from torchmetrics.regression import SymmetricMeanAbsolutePercentageError
import torch
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from darts import TimeSeries
from darts.metrics import smape

def initialize_and_compile_model(type_of_model: str, start_learning_rate=0.01, learning_rate_decay=True, batch_size=32, epochs=50, es_patience=7, accelerator="cpu"):

    #for TFT add:   num_attention_heads, lstm_layers, hidden_size   parameters

    my_stopper = EarlyStopping(
    monitor="val_loss",
    patience=es_patience,
    min_delta=0.005,
    mode='min',
    )

    pl_trainer_kwargs={"callbacks": [my_stopper],
                    "accelerator": accelerator}

    if learning_rate_decay:
        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau #reduce learning rate when a metric has stopped improving
    else:
        lr_scheduler = None

    if type_of_model == "RNN":
        model = BlockRNNModel(

        model = "LSTM",

        input_chunk_length=120,

        output_chunk_length=24,

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
        #Code for the TFT model here
        pass

    print("✅ Model initialized & compiled")

    return model



def train_model(model, type_of_model: str, y_train: TimeSeries, y_val: TimeSeries, past_covariates: TimeSeries, past_covariates_val: TimeSeries, future_covariates=None, future_covariates_val=None):


    if type_of_model == "RNN":
        model.fit(series=y_train,    # the target training data
            past_covariates=past_covariates,     # the multi covariate features training data
            val_series=y_val,  # the target validation data
            val_past_covariates=past_covariates_val,   # the multi covariate features validation data
            verbose=False)

    elif type_of_model == "TFT":
        model.fit(series=y_train,    # the target training data
            past_covariates=past_covariates,     # the multi covariate features training data
            val_series=y_val,  # the target validation data
            val_past_covariates=past_covariates_val,   # the multi covariate features validation data
            future_covariates=future_covariates,
            val_future_covariates=future_covariates_val,
            verbose=False)

    print(f"✅ Model trained on {y_train.duration}.")

    return model


def evaluate_model(true_series: TimeSeries, forecasted_series: TimeSeries) -> float:

    smape_score = smape(true_series, forecasted_series) # maybe change the metric !!

    print(f"✅ Model evaluated, SMAPE: {round(smape_score, 2)} %")

    return smape_score


def predict_next_24h(model, very_latest_time_series: TimeSeries, very_latest_past_covariates: TimeSeries) -> TimeSeries:

    prediction_series = model.predict(n=24, series=very_latest_time_series, past_covariates=very_latest_past_covariates) #Predict the n time step following the end of the training series, or of the specified series.

    return prediction_series

from darts.models import BlockRNNModel
from torchmetrics.regression import SymmetricMeanAbsolutePercentageError
import torch
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
#from cardano_crystal_ball.interface import preprocessor

def initialize_and_compile_model(type_of_model: str, start_learning_rate=0.01, learning_rate_decay=True, batch_size=32, epochs=50, es_patience=7, accelerator="cpu"):

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



def train_model(model, y, past_covariates, future_covariates=None):
    pass

def evaluate_model():
    pass

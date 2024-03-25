from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cardano_crystal_ball.interface.main import *
from sklearn.model_selection import train_test_split

app = FastAPI()

app.state.model = load_model()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/')
def predict():

    model = load_model()
    pred = model.predict(n = 24, series=None, past_covariates=None)
    return {'prediction': pred.values()[:, 0].tolist()}
    #return {'prediction': 'pred'}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cardano_crystal_ball.interface.main import *
from sklearn.model_selection import train_test_split
from cardano_crystal_ball.api.api_utils import *
from cardano_crystal_ball.ml_logic.registry import load_model

app = FastAPI()

app.state.model = load_model()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/predict')
def predict():

    #model = load_model()
    #print(type(app.state.model))
    pred = app.state.model.predict(n = 24)
    #return {'prediction': pred.values()[:, 0].tolist()}

    yesterdays_rate, yesterdays_start_time = get_yesterdays_rate(pred)
    return {#'prediction': pred.values()[:, 0].tolist(),
            'start_time': pred[0].time_index[0].strftime('%Y-%m-%d %H:%M:%S'),
            'yesterdays_rate': yesterdays_rate,
            'yesterdays_start_time': yesterdays_start_time,
            'upwards_trend': upwards_trend(pred)}

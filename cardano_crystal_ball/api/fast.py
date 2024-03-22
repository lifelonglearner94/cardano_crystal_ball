from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cardano_crystal_ball.ml_logic.model import *
app = FastAPI()

# app.state.model = initialize_and_compile_model('RNN')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get('/')
def predict():

    return {'prediction': 'comming soon! ;)'}

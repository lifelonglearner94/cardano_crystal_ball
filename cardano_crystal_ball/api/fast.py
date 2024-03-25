from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cardano_crystal_ball.interface.main import *

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
    csv_path = os.path.join(LOCAL_DATA_PATH,'processed', 'preprocess.csv')
    df = pd.read_csv(csv_path)


    X = df.drop(columns = ["rate"])#, "rate_scaled"])
    y = df[[ "rate"]]



    pred = app.state.model.predict(y)
    return {'prediction': pred}

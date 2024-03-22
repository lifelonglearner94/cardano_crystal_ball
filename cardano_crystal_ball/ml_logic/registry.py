from  cardano_crystal_ball.params import *
import time
from tensorflow import keras
import pickle
import glob



def load_model(stage ='Production'):
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    -
    -
    Return None  if no model is found
    """

    # TODO:
        #- load model from GCS (most recent one) if MODEL_TARGET=='gcs'
        #- load model from MLFLOW (by "stage") if MODEL_TARGET=='mlflow'

    if MODEL_TARGET == 'local':
        print('Load latest model from local')

        models_dir = os.PATH.join(LOC_REGISTRY_PATH, 'models')
        loc_model_paths = glob.glob(f"{models_dir}/*")

        if not loc_model_paths:
            return None

        latest_model_path = sorted(loc_model_paths)[-1]

        latest_model = keras.models.load(latest_model_path)
        print("✅ The latest model loaded from local disk")
        return latest_model


def save_model(model:keras.models = None):
    """
    - Save trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    -
    -
    """
    # TODO :
        #- if MODEL_TARGET='gcs', also save it in the bucket on GCS at "models/{timestamp}.h5"
        #- if MODEL_TARGET='mlflow', also save it on MLflow

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.PATH.join(LOC_REGISTRY_PATH, 'models', f'{timestamp}.h5')
    model.save(model_path)

    print("✅ Model saved locally")

def save_results(params:dict, metrics:dict):
    """
    - save params & metrics locally on the hard drive at
        "{LOCAL_REGISTRY_PATH}/params/{current_timestamp}.pickle"
        "{LOCAL_REGISTRY_PATH}/metrics/{current_timestamp}.pickle"
    -
    """
    # TODO:
        # if MODEL_TARGET='mlflow', also persist them on MLflow#


    timestamp = time.strftime("%Y%m%d-%H%M%S")

    if params is not None:
        params_path = os.path.join(LOC_REGISTRY_PATH, "params", timestamp + ".pickle")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)
        print("✅ Model's parameters saved locally")

    if metrics is not None:
        metrics_path = os.path.join(LOC_REGISTRY_PATH, "metrics", timestamp + ".pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)
        print("✅ Model's metrics saved locally")

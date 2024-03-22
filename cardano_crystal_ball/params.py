import os

MODEL_TARGET = os.environ.get("MODEL_TARGET")
LOC_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "cardano_crystal_ball")
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "cardano_crystal_ball", "data")

MODEL_TYPE = os.environ.get('MODEL_TYPE')

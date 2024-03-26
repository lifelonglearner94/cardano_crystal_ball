import os

MODEL_TARGET = os.environ.get("MODEL_TARGET")
LOC_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "cardano_crystal_ball")
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "cardano_crystal_ball", "data")

MODEL_TYPE = os.environ.get('MODEL_TYPE')
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_PROJECT_WAGON = os.environ.get("GCP_PROJECT_ID")
GCP_REGION = os.environ.get("GCP_REGION")
BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
INSTANCE = os.environ.get("INSTANCE")

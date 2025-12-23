import time
import os
import logging
from typing import List, Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import mlflow.pyfunc
import requests
import json



# logging setting
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# model loading
#os.environ["MLFLOW_TRACKING_URI"] = "http://127.0.0.1:5000"

MODEL_NAME = "FINAL_DEPLOYABLE_MODEL"
MODEL_STAGE = "Staging"
# MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_STAGE}"

# !!!!!!! after downloading mlflow model into a LOCAL path
#!!!!!!! for Docker contanerization
MODEL_URI = f"./{MODEL_NAME}_local"


# define model loading parameter

loaded_model: mlflow.pyfunc.PyFuncModel = None

DATA_API_BASE_URL = "http://127.0.0.1:8000"
####!!!!!!! for Docker contanerization
#DATA_API_BASE_URL = "http://localhost:8000"
DATA_RETRIEVAL_ENDPOINT = f"{DATA_API_BASE_URL}/api/v1/data_retrieval"
EXPECTED_INPUT_SHAPE = [1, 1, 28, 28]

class ImageIdRequest(BaseModel):

    image_id: int

class PredictionOutput(BaseModel):

    predicted_class: int
    time_ms: float


app = FastAPI(
    title="Full System PyTorch Model API",
    description="Serving PyTorch_Multi-View_Model with MLflow_Pyfunc"
)

@app.on_event("startup")

async def load_model_on_startup():

    global loaded_model
    try:
        logger.info(f"model loading URI: {MODEL_URI}")
        # full_pyfunc_model (model+signature) will be runned

        loaded_model = mlflow.pyfunc.load_model(MODEL_URI)
        logger.info("✅model is successfully runned")
    except Exception as e:
        logger.error(f"❌ loading error: {e}")

        raise RuntimeError(f"check mlflow registery parameters: Model_Name&Model_stage. Error: {e}")

@app.get("/health")

def health_check():

    if loaded_model is not None:

        return {"status": "ok", "model_loaded": True, "model_name": MODEL_NAME}
    else:

        raise HTTPException(status_code=503, detail="model has not been yet loaded")

@app.post("/predict", response_model=PredictionOutput)

def predict_endpoint(request: ImageIdRequest):


    if loaded_model is None:
        raise HTTPException(status_code=503, detail="model is not ready for be served")



    image_id = request.image_id
    logger.info(f"Received request for image_id: {image_id}")

    try:
        data_api_response = requests.post(
            DATA_RETRIEVAL_ENDPOINT,
            json={"image_id": image_id}
        )
        data_api_response.raise_for_status()


        retrieved_data = data_api_response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Data API for ID {image_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data from Feature Retrieval API.")

    # ----------------------------------------------------

    try:
        image_data_list = retrieved_data['image_data']
        model_input_array = np.array(image_data_list, dtype=np.float32)

        if model_input_array.shape != tuple(EXPECTED_INPUT_SHAPE):
             raise ValueError(f"Input shape mismatch. Expected {EXPECTED_INPUT_SHAPE}, got {model_input_array.shape}")

        wrapper_input = model_input_array


    except (ValueError, KeyError, AttributeError) as e:
        logger.error(f"Data processing error for ID {image_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Data format error during image processing: {e}")




    start_time = time.time()

    try:
        predictions = loaded_model.predict(wrapper_input)
    except Exception as e:
        logger.error(f"predict error for ID {image_id}: {e}")
        raise HTTPException(status_code=500, detail=f"model runnig error: {e}")

    end_time = time.time()

    predicted_class = int(np.argmax(predictions.flatten()))

    return PredictionOutput(
        predicted_class = predicted_class,
        time_ms=(end_time - start_time) * 1000
    )


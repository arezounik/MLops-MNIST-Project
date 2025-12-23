# Data_API.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Data_API_session import get_db
from Data_API_confirmator import ItemMetadata, DataRetrievalResponse, ItemRequest
from Data_API_basemodel import MetadataTable
from torchvision import datasets, transforms
import torch

app = FastAPI()


TRAIN_DATASET = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())
TEST_DATASET = datasets.MNIST(root="./data", train=False, download=True, transform=transforms.ToTensor())
TRAIN_SIZE = len(TRAIN_DATASET)

@app.post("/api/v1/Metadata", response_model=ItemMetadata)

def get_metadata_only(request: ItemRequest, db: Session = Depends(get_db)):

    metadata = db.query(MetadataTable).filter(

        MetadataTable.image_id == request.image_id

    ).first()


    if metadata is None:

        raise HTTPException(status_code=404, detail="Metadata not found for this image_id")

    return metadata


@app.post("/api/v1/data_retrieval", response_model=DataRetrievalResponse)
def get_data_for_inference(request: ItemRequest, db: Session = Depends(get_db)):

    image_id = request.image_id

    metadata = db.query(MetadataTable).filter(
        MetadataTable.image_id == image_id
    ).first()

    if metadata is None:
        raise HTTPException(status_code=404, detail="Metadata not found.")

    if metadata.data_split == "train":
        dataset_to_use = TRAIN_DATASET
    else:
        dataset_to_use = TEST_DATASET

    internal_index = metadata.data_index


    try:
        image_tensor, true_label = dataset_to_use[internal_index]
        batched_tensor = image_tensor[None, ...]
        image_data_list = batched_tensor.tolist()

        #NO Numpy
    except Exception as e:

        print(f"ERROR: Data retrieval failed for image ID {image_id}. Error details: {e}")

        raise HTTPException(status_code=500, detail=f"Internal data processing failed. Error: {e}")


    return DataRetrievalResponse(image_id=image_id, image_data=image_data_list)


from pydantic import BaseModel
from typing import List

class ItemMetadata(BaseModel):

    image_id: int

    label_class: int

    label_name: str

    file_path: str

    data_split: str

    data_index: int



class ItemRequest(BaseModel):

    image_id: int

#class DataRetrievalResponse(ItemMetadata):
class DataRetrievalResponse(BaseModel):

    image_id: int
    #***
    image_data: List[List[List[List[float]]]]

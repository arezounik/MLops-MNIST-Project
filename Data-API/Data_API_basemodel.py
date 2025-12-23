from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()


class MetadataTable(Base):
    __tablename__ = 'mnist_metadata'

    image_id = Column(Integer, primary_key=True)
    label_class = Column(Integer)
    label_name = Column(String(50))
    file_path = Column(String(255))
    data_split = Column(String(10))
    data_index = Column(Integer)

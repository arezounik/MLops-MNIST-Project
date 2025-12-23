# Metadata.pt


import pandas as pd
from sqlalchemy import create_engine
from torchvision import datasets, transforms
from urllib.parse import quote_plus
import torch
import os

#MySQL informations_for other people

MYSQL_USER = os.getenv("MYSQL_USER", "wsl_user")

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

MYSQL_HOST = os.getenv("MYSQL_HOST", "db")

MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

MYSQL_DB = os.getenv("MYSQL_DB", "mlops_db")



safe_password = quote_plus(MYSQL_PASSWORD)

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{safe_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

#datasets, download=False

train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transforms.ToTensor())
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transforms.ToTensor())

#creating two dataframes with pandas which include Metadata of datasets(labels, ...)


def extract_metadata(dataset, split_name, start_id):

    targets_list = dataset.targets.tolist()

    df = pd.DataFrame({
        'image_id': range(start_id, start_id + len(dataset)),

        'label_class': targets_list,

        'label_name': [str(i) for i in targets_list],

        'file_path': f'images/{split_name}/' + pd.Series(range(len(dataset))).astype(str) + '.png',

        'data_split': split_name ,

        'data_index': list(range(len(dataset)))

    })
    return df


train_df = extract_metadata(train_dataset, 'train', 0)
test_df = extract_metadata(test_dataset, 'test', len(train_dataset))

#concatenate dataframes
full_metadata_df = pd.concat([train_df, test_df], ignore_index=True)

#upload the dataframe into the MySQL's database

try:
    engine = create_engine(DATABASE_URL)

    full_metadata_df.to_sql(
        name='mnist_metadata',
        con=engine,
        if_exists='replace',
        index=False
    )
    print(f"Metadata for both Train and Test successfully inserted into MySQL table **'mnist_metadata'**.")

except Exception as e:
    print(f"Error connecting to or inserting data into MySQL: {e}")

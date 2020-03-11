from minio import Minio
from minio.error import ResponseError
import uuid
import os

import logging

BUCKET_NAME = 'renews'


def store_string(minio: Minio, body: str, minio_file: str):
    # create a file
    filename_server = "./tmp/%s.txt" % str(uuid.uuid4())
    with open(filename_server, "w") as f:
        f.write(body)

    # store it in minio
    try:
        minio.fput_object(bucket_name=BUCKET_NAME, object_name=minio_file, file_path=filename_server)
    except ResponseError as err:
        print(err)

    # delete file from server
    os.remove(filename_server)
    return


def get_string(minio: Minio, minio_file: str):
    # get file from minio
    filename_server = "./tmp/%s.txt" % str(uuid.uuid4())
    try:
        minio.fget_object(BUCKET_NAME, minio_file, filename_server)
    except ResponseError as err:
        print(err)

    # file to string
    with open(filename_server, 'r') as file:
        data = file.read()

    # delete file from server
    os.remove(filename_server)
    return data


def delete_object(minio: Minio, minio_file: str):
    minio.remove_object(BUCKET_NAME,minio_file)

    return

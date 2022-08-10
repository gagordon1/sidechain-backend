from webbrowser import get
from aws_controller import delete_file_from_aws_bucket, delete_record
from config import AWS_S3_BUCKET_ADDRESS
import sys

def delete_sidechain(id):
    """Given a sidechain metadata id, delete the underlying files
    then metadata record from AWS

    Args:
        id str: unique id for a sidechain metadata
    """
    for content in ["image", "artwork", "project_files"]:
        delete_file_from_aws_bucket(id + "/" + content)
    delete_record(id)


if __name__ == "__main__":
    id = sys.argv[1]
    delete_sidechain(id)
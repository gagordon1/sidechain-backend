import boto3
from config import AWS_REGION, AWS_METADATA_TABLE_NAME
import time


def upload_metadata_to_database(id, description, image, name, artwork, project_files):
    """Uploads a metadata record to metadata database

    Args:
        id uuid: id for the metadata file
        description str: description of the artwork
        image str | None: link to hosted image file
        name str: name of the artwork
        artwork str: link to artwork file
        project_files str | None: link to hosted project zip file
    
    Raises:
        Error: Error when uploading to database
    """
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
    dynamodb.put_item(TableName=AWS_METADATA_TABLE_NAME,
         ReturnValues="ALL_OLD",
         Item={
            'id':{'S':id},
            'description':{'S':description},
            'image':{'S':image},
            'name':{'S':name},
            'artwork':{'S':artwork},
            'project_files':{'S':project_files},
            'timestamp_added':{'N' : str(time.time())}
        }
    )

def upload_file_to_aws_bucket(path, data):
    """Uploads a file to aws bucket at a specified path

    Args:
        path str: path to the file in bucket
        data file: any file

    Returns:
        str: link to the hosted file
    """
    pass

def get_metadata_from_aws_bucket(id):
    """_summary_

    Args:
        id str: unique id for a contract address's metadata

    Returns:
        object: metadata of the format sidechain_metadata_standard.json
    """
    pass


def delete_record(id):
    """Deletes a sidechain metadata record along with the files it points to

    Args:
        id str: unique id for a sidechain record

    Raises:
        Exception : Exception while attempting to delete a file

    Returns:
        boolean: true on successful deletion, false if id not found
    """
    pass
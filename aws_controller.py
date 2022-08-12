import boto3
from config import AWS_REGION, AWS_METADATA_TABLE_NAME, AWS_BUCKET, AWS_S3_BUCKET_ADDRESS

def get_all_records():
    """Gets all ids in the system.
    """
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(AWS_METADATA_TABLE_NAME)
    return map(lambda x : x["id"], table.scan()["Items"])

    


def upload_metadata_to_database(id, description, image, name, artwork, project_files, timestamp):
    """Uploads a metadata record to metadata database

    Args:
        id uuid: id for the metadata file
        description str: description of the artwork
        image str | None: link to hosted image file
        name str: name of the artwork
        artwork str: link to artwork file
        project_files str | None: link to hosted project zip file
        timestamp str : timestamp added
    
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
            'timestamp_added':{'N' : timestamp}
        }
    )

def upload_file_to_aws_bucket(path, data, content_type):
    """Uploads a hosted file to aws bucket

    Args:
        path str: path to the file in bucket
        data bytes: bytes object
        content_type str: valid mimetype (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
    """
    s3 = boto3.resource('s3')
    result = s3.Bucket(AWS_BUCKET).Object(path).put(Body=data, ContentType=content_type)
    return AWS_S3_BUCKET_ADDRESS + "/" + path

def get_metadata_from_aws_bucket(id):
    """_summary_

    Args:
        id str: unique id for a contract address's metadata
    
    Raises:
        Exception : if item is not found.

    Returns:
        object: metadata of the format sidechain_metadata_standard.json
    """
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
    result = dynamodb.get_item(TableName=AWS_METADATA_TABLE_NAME,
        Key={
            "id" : {"S" : id}
        }
    )
    item = result["Item"]
    return {
        "description" : item["description"]["S"],
        "external_url" : "",
        "image" : item["image"]["S"],
        "name" : item["name"]["S"],
        "asset_specific_data" : {
            "project_files" : item["project_files"]["S"],
            "artwork" : item["artwork"]["S"],
            "timestamp" : item["timestamp_added"]["N"]
        }
    }


def delete_record(id):
    """Deletes a sidechain metadata record along with the files it points to

    Args:
        id str: unique id for a sidechain record

    Raises:
        Exception : Exception while attempting to delete a file

    Returns:
        boolean: true on successful deletion, false if id not found
    """
    dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
    result = dynamodb.get_item(TableName=AWS_METADATA_TABLE_NAME,
        Key={
            "id" : {"S" : id}
        }
    )
    if "Item" in result:
        dynamodb.delete_item(TableName=AWS_METADATA_TABLE_NAME,
            Key={
                'id' : {'S' : id}
            }
        )
        return True
    return False

def delete_file_from_aws_bucket(path):
    """Deletes a file given a path within an AWS S3 bucket if it exists

    Args:
        path str: path to an S3 file for a bucket
    
    Raises:
        Exception : Exception while attempting to delete a file
    """
    s3 = boto3.resource('s3')
    result = s3.Bucket(AWS_BUCKET).Object(path).delete()
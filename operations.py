from aws_controller import upload_metadata_to_database, upload_file_to_aws_bucket, get_metadata_item
from config import METADATA_SERVER
import time

default_content_types = {
    "artwork" : "audio/mpeg",
    "image" : "image/jpeg"
}

   
def upload_to_aws(artwork, name, description, image, project_files, id, auth_token, content_types = default_content_types):
    artwork_link = upload_file_to_aws_bucket(id + "/artwork", artwork.read(), content_types["artwork"])
    image_link = ""
    project_files_link = ""
    if image:
        image_link = upload_file_to_aws_bucket(id + "/image", image.read(), content_types["image"])
    if project_files:
        project_files_link = upload_file_to_aws_bucket(id + "/project_files", project_files.read(), "application/zip")
    upload_metadata_to_database(id, description, image_link, name, artwork_link, project_files_link, auth_token, str(time.time()))
    return METADATA_SERVER + "/" + id + "/"


def valid_auth_token(id, auth_token):
    """Returns true if auth_token is valid for an id

    Args:
        id str: metadata id
        auth_token str: authorization to update metadata
    """
    item  = get_metadata_item(id)
    return item["auth_token"]["S"] == auth_token
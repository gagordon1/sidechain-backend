from aws_controller import upload_metadata_to_database, upload_file_to_aws_bucket
from config import METADATA_SERVER
import uuid
import time

default_content_types = {
    "artwork" : "audio/mpeg",
    "image" : "image/jpeg"
}
def upload_to_aws(artwork, name, description, image, project_files, id, content_types = default_content_types):

    print(id)
    # #upload files to aws
    artwork_link = upload_file_to_aws_bucket(id + "/artwork", artwork.read(), content_types["artwork"])
    image_link = ""
    project_files_link = ""
    if image:
        image_link = upload_file_to_aws_bucket(id + "/image", image.read(), content_types["image"])
    if project_files:
        project_files_link = upload_file_to_aws_bucket(id + "/project_files", project_files.read(), "application/zip")

    #upload metadata file
    upload_metadata_to_database(id, description, image_link, name, artwork_link, project_files_link, str(time.time()))
    return METADATA_SERVER + "/" + id + "/"
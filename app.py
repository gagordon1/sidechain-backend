
from flask import Flask, request
from flask_cors import CORS
from aws_controller import upload_metadata_to_database, get_metadata_from_aws_bucket, upload_file_to_aws_bucket
from config import METADATA_SERVER
import uuid
import time

PORT = 8080
app = Flask(__name__)
CORS(app)

"""
GET
    Gets metadata for a contract address
    id : str metadata id for a contract
    token_id : int
    returns Sidechain Metadata
"""
@ app.route("/<id>/<token_id>", methods=["GET"])
def metadata(id, token_id):
    try:
        return get_metadata_from_aws_bucket(id)
    except:
        return "Could not get metadata for the given URI", 400

"""
POST
    Uploads a new sidechain metadata file
    Uses the Opensea standard
    

    image : image file (tested for .jpeg) 
    description : str 
    name : str 
    project_files : zip file
    artwork : file tested for (.mp3, .wav)

    responds with base uri on success (with trailing /)

    400 : artwork parameter is missing
"""
@ app.route("/upload", methods=["POST"])
def upload_metadata():
    try:
        artwork = request.files["artwork"]
        name = request.form["name"]
        description = request.form["description"]
        image = None
        project_files = None
        if "image" in request.files:
            image = request.files["image"]
        if "project_files" in request.files:
            project_files = request.files["project_files"]

        id = str(uuid.uuid4())
        # #upload files to aws
        artwork_link = upload_file_to_aws_bucket(id + "/artwork", artwork.read(), artwork.content_type)
        image_link = ""
        project_files_link = ""
        if image:
            image_link = upload_file_to_aws_bucket(id + "/image", image.read(), image.content_type)
        if project_files:
            project_files_link = upload_file_to_aws_bucket(id + "/project_files", project_files.read(), project_files.content_type)

        #upload metadata file
        upload_metadata_to_database(id, description, image_link, name, artwork_link, project_files_link, str(time.time()))
        return METADATA_SERVER + "/" + id + "/"
    except Exception as e:
        print(e)
        return "Error in request", 400


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
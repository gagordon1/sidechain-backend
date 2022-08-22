from flask import Flask, request
from flask_cors import CORS
from aws_controller import get_metadata_from_aws_bucket, update_metadata_post_deployment, query_sidechain
from operations import upload_to_aws, valid_auth_token
from config import SIDECHAIN_BASE_URL
import uuid


PORT = 8000
app = Flask(__name__)
CORS(app, origins=[SIDECHAIN_BASE_URL])


"""
GET
    Gets metadata for a contract address
    id : str metadata id for a contract
    token_id : int
    returns Sidechain Metadata

POST
    Updates external url in metadata file for a metadata id
    request.data : {contract address}%{authToken} (text/plain)

    400 error if authToken is invalid.
"""
@ app.route("/<id>/<token_id>", methods=["GET", "POST"])
def metadata(id, token_id):
    if request.method == "GET":
        try:
            return get_metadata_from_aws_bucket(id)
        except Exception as e:
            print(e)
            return "Could not get metadata for the given URI", 400
    elif request.method == "POST":
        try:
            data = request.data.decode('utf-8')
            [address, auth_token] = data.split("%")
            if (valid_auth_token(id, auth_token)):
                return update_metadata_post_deployment(id, SIDECHAIN_BASE_URL + "/artwork/" + address, address)
            else:
                return "Not authorized to update metadata", 400
        except Exception as e:
            print(e)
            return "Could not update external url", 400



"""
POST
    Uploads a new sidechain metadata file
    Uses the Opensea standard
    

    image : image file (tested for .jpeg) 
    description : str 
    name : str 
    project_files : zip file
    artwork : file tested for (.mp3, .wav)

    responds with {base_uri with trailing /}%authToken on valid upload

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
        authToken = str(uuid.uuid4())
        baseURI = upload_to_aws(artwork, name, description, image, project_files, id, authToken)
        return baseURI + '%' + authToken
    except Exception as e:
        print(e)
        return "Error in request", 400


"""Gets all sidechains in the metadata database.

    sort : str [timestamp_asc, timestamp_desc]
    keyword : str 
    limit : int number to return
    offset : int index to start pulling from 
"""
@ app.route("/feed", methods=["GET"])
def get_sidechains():
    try:
        offset = int(request.args.get('offset'))
        limit = int(request.args.get('limit'))
        return query_sidechain(request.args.get('sort'), request.args.get('keyword'),limit + offset, offset)
    except Exception as e:
        print(e)
        return "Could not get feed", 400


if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
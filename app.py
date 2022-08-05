from flask import Flask, request, redirect, g, render_template, jsonify
import json
import requests

PORT = 8080
app = Flask(__name__)

"""
GET
    Gets metadata for a contract address
    contract_address : str
    returns Sidechain Metadata
"""
@ app.route("/:contract_address/:token_id", methods=["GET"])
def metadata(contract_address):
    pass


"""
For a wallet address, get a list of contracts where they’ve downloaded stems
along with time of download
    wallet_address : Wallet Address
    returns [{contract_address : Contract Address, timestamp : int}] 
"""
@ app.route("/downloads/:wallet_address", methods=["GET"])
def get_downloads(wallet_address):
    pass



"""
authorization required
Downloads stems and adds contract to a wallets’ list of downloads
    body: 
        wallet_address : Wallet Address
        contract_address : Contract Address
    returns [{track_name : String, file : File Link}]
"""
@ app.route("/download", methods = ["POST"])
def download_stems():
    pass

"""
Gets a list of contract addresses
    params :
        sort : “trending” | “recent” | “top”
        search : String
        limit : int (default : 30)
        offset : int (default : 0) 
    returns [Contract Address]
"""
@ app.route("/works", methods = ["GET"])
def get_works():
    pass


#authorization required
"""
Posts a comment to a contract address
    body :
        wallet_address : Wallet Address
        contract_address : Contract Address
        text : String
"""
@ app.route("/comment", methods = ["POST"])
def comment_work():
    pass


#authorization required
"""
Likes a contract address
    body :
        wallet_address : Wallet Address
        contract_address : Contract Address
"""
@ app.route("/like", methods = ["POST"])
def like_work():
    pass

"""
Given a user, get collection of created works
    user : Wallet Address
    returns  [Contract Address]
"""
@ app.route("/works/:user", methods = ["GET"])
def get_works_by_user(user):
    pass


"""
Given required metadata params, create a work
    body:
        data : Sidechain Metadata
"""
@ app.route("/upload", methods = ["POST"])
def upload_work():
    pass






if __name__ == "__main__":
    app.run(debug=True, port=PORT)
from dotenv import load_dotenv
import os
load_dotenv()


DEVELOPMENT = False

if DEVELOPMENT:
    SIDECHAIN_BASE_URL = "http://localhost:3000"
    METADATA_SERVER = "http://localhost:8000"
    AWS_METADATA_TABLE_NAME = "Sidechain"
else:
    SIDECHAIN_BASE_URL = "https://www.side-chain.xyz"
    METADATA_SERVER = "https://sidechain-backend.herokuapp.com"
    AWS_METADATA_TABLE_NAME = "Sidechain-Test-Network" #running on Rinkeby

AWS_S3_BUCKET_ADDRESS = os.getenv("AWS_BUCKET_ADDRESS")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_BUCKET = os.getenv("BUCKET_NAME")

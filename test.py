from email.mime import image
from aws_controller import upload_file_to_aws_bucket, upload_metadata_to_aws_bucket, get_metadata_from_aws_bucket
from config import SIDECHAIN_BASE_URL
import requests

test_data_1 = {
        "id" : 1,
        "description" : "test data 1",
        "image" : "https://www.google.com",
        "name" : "Artwork 1",
        "artwork" : "https://www.google.com/maps",
        "project_files" : "https://www.google.com/docs"
    }

def run_aws_controller_tests():
    """
    Strategy:
        1. Test upload_metadata_to_aws_bucket, delete_record and
        get_metadata_from_aws_bucket automatically
        2. Test upload_file_to_aws_bucket manually checking that files are intact in their buckets
    """
    def test_metadata():
        print("\ttest1...")
        for test_data in [test_data_1]:
            id = test_data["id"]
            description = test_data["description"]
            image = test_data["image"]
            name = test_data["name"]
            artwork = test_data["artwork"]
            project_files = test_data["project_files"]
            link = upload_metadata_to_aws_bucket(id, description, image, name, artwork, project_files)
            expected = {
                "description" : description,
                "external_url" : SIDECHAIN_BASE_URL + "/artwork/" + id,
                "image" : image,
                "name" : name,
                "asset_specific_data" : {
                    "project_files" : project_files,
                    "artwork" : artwork
                }
            }
            response = requests.get(link)
            assert response.data == expected, "metadata was different than expected"




    
    print("Test Metadata\n")
    test_metadata()





if __name__ == "__main__":
    run_aws_controller_tests()

    

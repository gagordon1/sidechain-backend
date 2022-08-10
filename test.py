from cgi import test
from email.mime import image
from urllib import response
from aws_controller import delete_record, upload_metadata_to_database, get_metadata_from_aws_bucket, upload_file_to_aws_bucket, delete_file_from_aws_bucket
from config import AWS_REGION, AWS_METADATA_TABLE_NAME, AWS_S3_BUCKET_ADDRESS
import requests
import boto3

test_data_1 = {
        "id" : "1",
        "description" : "test data 1",
        "image" : "https://www.google.com",
        "name" : "Artwork 1",
        "artwork" : "https://www.google.com/maps",
        "project_files" : "https://www.google.com/docs"
    }

test_data_2 = {
        "id" : "2",
        "description" : "",
        "image" : "",
        "name" : "",
        "artwork" : "https://www.google.com/maps",
        "project_files" :""
    }
def passed():
    print("\t\tpassed!")

def run_aws_controller_tests():
    """
    Strategy:
        1. Test upload_metadata_to_aws_bucket, delete_record and
        get_metadata_from_aws_bucket automatically
        2. Test upload_file_to_aws_bucket manually checking that files are intact in their buckets
    """
    def test_metadata():
        print("\ttest1...")
        for test_data in [test_data_1, test_data_2]:
            id = test_data["id"]
            description = test_data["description"]
            image = test_data["image"]
            name = test_data["name"]
            artwork = test_data["artwork"]
            project_files = test_data["project_files"]
            upload_metadata_to_database(id, description, image, name, artwork, project_files)
            dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)
            result = dynamodb.get_item(TableName=AWS_METADATA_TABLE_NAME,
                Key={
                    "id" : {"S" : id}
                }
            )
            item = result["Item"]
            for attr in test_data:
                assert test_data[attr] == item[attr]['S'], "Value in database for {attr} was incorrect."
        passed()
        
        print("\ttest2...")
        for test_data in [test_data_1, test_data_2]:
            id = test_data["id"]
            description = test_data["description"]
            image = test_data["image"]
            name = test_data["name"]
            artwork = test_data["artwork"]
            project_files = test_data["project_files"]
            expected = {
                "description" : description,
                "external_url" : "",
                "image" : image,
                "name" : name,
                "asset_specific_data" : {
                    "project_files" : project_files,
                    "artwork" : artwork
                }
            }
            metadata = get_metadata_from_aws_bucket(id)
            assert metadata == expected, "metadata was different than expected"
        passed()

        print("\ttest3...")
        for test_data in [test_data_1, test_data_2]:
            id = test_data["id"]

            assert delete_record(id), "could not find and delete record"
        
        assert not delete_record("3"), "deleting a nonexistent file did not return false"
        passed()

    """
    Strategy:
        Test uploading and deleting files
    """
    def test_file_upload():
        file_path = "test_file_1"
        data = "hello"
        content_type = "text/plain"
        print("\ttest1...")
        upload_file_to_aws_bucket(file_path, data, content_type)
        response = requests.get(AWS_S3_BUCKET_ADDRESS + "/" + file_path)
        assert response.text == data, "file was not correctly uploaded"
        passed()


        print("\ttest2...")
        delete_file_from_aws_bucket(file_path)
        response = requests.get(AWS_S3_BUCKET_ADDRESS + "/" + file_path)
        assert response.status_code == 403, "request to deleted file did not error out"
        passed()



    
    # print("Test Metadata\n")
    # test_metadata()

    print("Test File Upload\n")
    test_file_upload()





if __name__ == "__main__":
    run_aws_controller_tests()

    

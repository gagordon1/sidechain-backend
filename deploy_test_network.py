from os import listdir
from operations import upload_to_aws


def deploy_test_network():

	TEST_FILE_DIRECTORY = "./test_files"
	for title in listdir(TEST_FILE_DIRECTORY):
		print(title)
		if title != ".DS_Store":
			project_dir = TEST_FILE_DIRECTORY + "/" + title
			artwork = open(project_dir + "/master.mp3", "rb")
			try:
				image = open(project_dir + "/artwork.jpg", "rb")
			except Exception as e:
				image = None
			
			project_files = open(project_dir + "/project_files.zip", "rb")
			description = "This is a description for {}. Remixes of this work will automatically allocate the specified REV percentage of tokens to this contract's creator upon minting.".format(title)
			name = title
			link = upload_to_aws(artwork, name, description, image, project_files, id="test-{}".format(title))
			print("\tbaseURI: {}".format(link))

if __name__ == '__main__':
	deploy_test_network()
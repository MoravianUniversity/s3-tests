import boto3
import os


def upload_to_s3(s3, local_file, s3_key):
    '''
    upload the file to s3 bucket
    parameters:
        local_file: the absolute path of the file to upload
        s3_key: the relative path of the file within the [local_file] directory
    '''
    bucket_name = "mirrulations-test-bucket"

    s3.upload_file(local_file, bucket_name, s3_key)


def main():
    '''
    get each file in the data directory and its relative path within the directory
    uses the relative path as the file's s3 key.
    '''
    session = boto3.Session(profile_name="mirrulations_client")
    s3 = session.client("s3")

    data_dir = os.path.expanduser("~/data/data") # get the absolute path of the data directory
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            local_path = os.path.join(root, filename) # get the full absolute path of the file
            s3_path = os.path.relpath(local_path, data_dir) # get the relative path of the file from within the data directory 
            upload_to_s3(s3, local_path, s3_path)


if __name__ == "__main__":
    main()
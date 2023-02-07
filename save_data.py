import requests
import boto3
import json

DOCS = "https://api.regulations.gov/v4/documents"



def main():
    if check_for_s3_connection():
        put_results_s3(get_docs(), "mirrulations-test-bucket", "test.json")
    else:
        print("No connection to s3")


def get_key():
    """
    Gets the api key from the file
    """
    with open("API_KEY.txt", "r") as f:
        return f.read()


def get_docs():
    response = requests.get(DOCS, params={"api_key": get_key()})
    return response.json()


def put_results_s3(data, bucket_name, file_path):
    """
    Puts the results in an s3 bucket.
    Parameters
    ----------
    data : dict
        the data to be stored
    bucket_name : str
        name of the bucket
    file_path : str
        the file name to write as
    """
    session = boto3.Session(profile_name="mirrulations_client")
    s_3 = session.client("s3")
    json_data = json.dumps(data)
    print(json_data)
    try:
        s_3.put_object(Bucket=bucket_name, Key=file_path, Body=json_data)
    except Exception as e:
        print(e)


# Credientals folder is still missing such as ~/.aws/credentials
def check_for_s3_connection():
    """
    Checks if a valid connection could be made to s3
    """
    try:
        session = boto3.Session(profile_name="mirrulations_client")
        s_3 = session.client("s3")
        connection = s_3.list_buckets()
        return connection["ResponseMetadata"]["HTTPStatusCode"] == 200
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()
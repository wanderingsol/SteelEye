import boto3
import logging
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = ""
SECRET_KEY = ""
AWS_BUCKET = ""


class AWSConnector(object):
    def __init__(self, bucket=AWS_BUCKET, access_key=ACCESS_KEY, secret_key=SECRET_KEY):
        self.s3 = boto3.client(
            's3', aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )
        self.bucket = bucket

    def upload_file_to_bucket(self, file_path, file_name):
        try:
            self.s3.upload_file(file_path, self.bucket, file_name)
            logging.info(f"Uploaded {file_path} to AWS S3 {self.bucket}/{file_name}")
            return True
        except FileNotFoundError:
            logging.error(f"{file_path} does not exist")
            return False
        except NoCredentialsError:
            logging.error("Invalid credentials")
            return False

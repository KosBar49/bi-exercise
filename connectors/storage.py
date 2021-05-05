import boto3
import botocore

class StorageConnection():

    connection = None

    @classmethod
    def connect(cls):
        """ Create new connection to storage """
        if cls.connection is None:
            cls.connection = boto3.resource('s3')
        return cls.connection
    
    @classmethod
    def download_file(cls, bucket_name, key, local_name):
        """ Download file from the bucket """
        connection = cls.connect()
        try:
            connection.Bucket(bucket_name).download_file(key, local_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise e


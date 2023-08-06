"""Common s3 functions
"""
import boto3
import json
import os
from botocore.exceptions import ClientError


class S3Util:

    def __init__(self):
        self.s3 = boto3.resource('s3')

    def prefix(self, key):
        if os.environ.get('S3_PREFIX') is None:
            return key
        else:
            return f"{os.environ.get('S3_PREFIX')}/{key}"

    def bucket_name(self):
        if os.environ.get('S3_BUCKET') is None:
            raise ValueError('S3_BUCKET environment variable not set')
        return os.environ.get('S3_BUCKET')

    def exists(self, key):
        try:
            client = boto3.client('s3')
            client.head_object(Bucket=self.bucket_name(), Key=self.prefix(key))
            return True
        except ClientError:
            return False

    def read_json(self, key):
        return json.loads(self.read_file(key))

    def write_json(self, key, data):
        self.write_file(key, json.dumps(data))

    def read_file(self, key):
        obj = self.s3.Object(self.bucket_name(), self.prefix(key))
        return obj.get()['Body'].read().decode('utf-8')

    def write_file(self, key, data):
        self.s3.Object(self.bucket_name(), self.prefix(key)).put(Body=data)

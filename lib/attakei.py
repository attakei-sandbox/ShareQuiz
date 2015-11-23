# -*- coding:utf8 -*-
"""
"""
from __future__ import unicode_literals
import boto3
from botocore.exceptions import ClientError
import zipfile
import json


__author__ = 'attakei'


class S3Object(object):
    def __init__(self, region, bucket, key):
        self.region = region
        self.bucket = bucket
        self.key = key


def lambda_handler(event, context):
    """Updates function from lambda
    """
    records = event.get('Records', [])
    print(records)
    for record in records:
        if record['eventSource'] != 'aws:s3':
            print('pass')
        s3_object = S3Object(record['awsRegion'], record['s3']['bucket']['name'], record['s3']['object']['key'])
        print(record)
        _update_functions('sharequiz', 'test', s3_object)


def _update_functions(project, env, s3_object):
    project_zip_path = '/tmp/project.zip'
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_object.bucket)
    bucket.download_file(s3_object.key, project_zip_path)

    with zipfile.ZipFile(project_zip_path) as zfp:
        handlers_json = zfp.read('handlers.json')
    handlers_info = json.loads(handlers_json)

    _lambda = boto3.client('lambda')
    for handler in handlers_info['handlers']:
        for key, val in handlers_info['_default_'].items():
            handler.setdefault(key, val)
        handler['FunctionName'] = 'sharequiz-test-' + handler['FunctionName']
        handler['Code'] = {
            'S3Bucket': s3_object.bucket,
            'S3Key': s3_object.key,
        }
        try:
            _lambda.create_function(**handler)
        except ClientError as err:
            _lambda.update_function_code(
                FunctionName=handler['FunctionName'],
                S3Bucket=s3_object.bucket,
                S3Key=s3_object.key,
            )

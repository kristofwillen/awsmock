import pytest
import pydantic
import json
from typing import List

aws_region = "eu-west-1"

class Bucket(pydantic.BaseModel):
    name: str
    creationdate: str

@pytest.fixture
def s3_infra(s3_client):
    s3_client.create_bucket(
        Bucket='test-bucket1', 
        CreateBucketConfiguration={
          'LocationConstraint': aws_region
        })
    s3_client.create_bucket(
        Bucket='test-bucket2', 
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-1'
        })


@pytest.fixture
def kms_infra(kms_client):
    kms_client.create_key(
        Description='string',
        KeyUsage='ENCRYPT_DECRYPT',
        CustomerMasterKeySpec='SYMMETRIC_DEFAULT',
        KeySpec='SYMMETRIC_DEFAULT',
        Origin='AWS_KMS'
    )
    kms_client.create_key(
        Description='string',
        KeyUsage='ENCRYPT_DECRYPT',
        CustomerMasterKeySpec='SYMMETRIC_DEFAULT',
        KeySpec='SYMMETRIC_DEFAULT',
        Origin='AWS_KMS'
    )


def test_s3_bucket(s3_client, s3_infra):
    resp = s3_client.list_buckets()
    assert len(resp['Buckets']) == 2


def test_kms(kms_client, kms_infra):
    resp = kms_client.list_keys()
    print(json.dumps(resp, indent=4))
    assert len(resp['Keys']) == 2
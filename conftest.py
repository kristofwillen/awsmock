import boto3
import pytest
import os

from moto import mock_s3, mock_kms

aws_region = "eu-west-1"


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_ID"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        s3 = boto3.client("s3", region_name=aws_region)
        yield s3


@pytest.fixture
def kms_client(aws_credentials):
    with mock_kms():
        kms = boto3.client("kms", region_name=aws_region)
        # response = kms.create_key(
        #     Description='string',
        #     KeyUsage='ENCRYPT_DECRYPT',
        #     CustomerMasterKeySpec='SYMMETRIC_DEFAULT',
        #     KeySpec='SYMMETRIC_DEFAULT',
        #     Origin='AWS_KMS',
        # )
        # response = kms.create_key(
        #     Description='string',
        #     KeyUsage='ENCRYPT_DECRYPT',
        #     CustomerMasterKeySpec='SYMMETRIC_DEFAULT',
        #     KeySpec='SYMMETRIC_DEFAULT',
        #     Origin='AWS_KMS',
        # )

        yield kms

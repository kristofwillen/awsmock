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
        Bucket="test-bucket1",
        CreateBucketConfiguration={"LocationConstraint": aws_region},
    )
    s3_client.put_bucket_encryption(
        Bucket="test-bucket1",
        ContentMD5="string",
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms",
                        "KMSMasterKeyID": "695393b8-d577-429e-89a2-f9e46ad28faf",
                    },
                    "BucketKeyEnabled": True,
                },
            ]
        },
    )

    s3_client.create_bucket(
        Bucket="test-bucket2",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )
    s3_client.put_bucket_encryption(
        Bucket="test-bucket2",
        ContentMD5="string",
        ServerSideEncryptionConfiguration={
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "aws:kms",
                        "KMSMasterKeyID": "714a126c-49c8-4ecd-83ca-10d65c9029f6",
                    },
                    "BucketKeyEnabled": True,
                },
            ]
        },
    )


@pytest.fixture
def kms_infra(kms_client):
    kms_client.create_key(
        Description="string",
        KeyUsage="ENCRYPT_DECRYPT",
        CustomerMasterKeySpec="SYMMETRIC_DEFAULT",
        KeySpec="SYMMETRIC_DEFAULT",
        Origin="AWS_KMS",
    )
    kms_client.create_key(
        Description="string",
        KeyUsage="ENCRYPT_DECRYPT",
        CustomerMasterKeySpec="SYMMETRIC_DEFAULT",
        KeySpec="SYMMETRIC_DEFAULT",
        Origin="AWS_KMS",
    )


def test_s3_bucket(s3_client, s3_infra):
    resp = s3_client.list_buckets()
    print(resp["Buckets"])
    assert len(resp["Buckets"]) == 2


def test_kms(kms_client, kms_infra):
    resp = kms_client.list_keys()
    print(resp["Keys"])
    print(json.dumps(resp, indent=4))
    assert len(resp["Keys"]) == 2


def test_bucket_encr(s3_client, s3_infra):
    for b in ["test-bucket1", "test-bucket2"]:
        response = s3_client.get_bucket_encryption(Bucket=b)
        assert (
            response["ServerSideEncryptionConfiguration"]["Rules"][0][
                "ApplyServerSideEncryptionByDefault"
            ]["SSEAlgorithm"]
            == "aws:kms"
        )

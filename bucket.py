import json
import pydantic
import boto3
from typing import List, Optional
from datetime import datetime


class Tag(pydantic.BaseModel):
    Value: str
    Key: str


class ApplyServerSideEncryptionByDefault(pydantic.BaseModel):
    SSEAlgorithm: str
    KMSMasterKeyID: Optional[str]


class ServerSideEncryptionRule(pydantic.BaseModel):
    BucketKeyEnabled: Optional[bool]
    ApplyServerSideEncryptionByDefault: Optional[ApplyServerSideEncryptionByDefault]


class ServerSideEncryptionConfiguration(pydantic.BaseModel):
    Rules: List[ServerSideEncryptionRule]


class BucketEncryption(pydantic.BaseModel):
    ServerSideEncryptionConfiguration: ServerSideEncryptionConfiguration


# class Bucket(pydantic.BaseModel):
#     BucketName: Optional[str] = None
#     BucketEncryption: Optional[BucketEncryption] = None
#     CreationDate: Optional[datetime]
#     Tags: Optional[List[Tag]] = None


class Bucket(pydantic.BaseModel):
    Name: str
    CreationDate: Optional[datetime]
    SSEAlgorithm: Optional[str]
    Region: Optional[str]


def filter_buckets(buckets: List[Bucket], key, value) -> List[Bucket]:
    return list(filter(lambda x: x.__getattribute__(key) == value, buckets))


def startswith_buckets(buckets: List[Bucket], key, value) -> List[Bucket]:
    return list(filter(lambda x: x.__getattribute__(key).startswith(value), buckets))


def get_nr_of_cdh_buckets(buckets: List[Bucket]) -> int:
    return len(startswith_buckets(buckets, "Name", "cdh-"))


def get_nr_of_cdhlog_buckets(buckets: List[Bucket]) -> int:
    return len(startswith_buckets(buckets, "Name", "cdh-log"))


def get_bucket_encryption_and_location(s3_client, buckets):
    for i, b in enumerate(buckets):
        nrofbuckets = len(buckets)
        if b.Name.startswith("cdh"):
            try:
                resp = s3_client.get_bucket_encryption(Bucket=b.Name)
            except Exception as e:
                print(f"[WARN] Cannot get bucket encryption => {e}")
            else:
                # print(json.dumps(resp, indent=4))
                bucket_encr = BucketEncryption(**resp)
                # print(bucket_encr.ServerSideEncryptionConfiguration.Rules[0])
                b.SSEAlgorithm = bucket_encr.ServerSideEncryptionConfiguration.Rules[
                    0
                ].ApplyServerSideEncryptionByDefault.SSEAlgorithm
                # print(b.SSEAlgorithm)
                print(
                    f"[{i}/{nrofbuckets}] {b.Name.ljust(50,' ')}: {b.SSEAlgorithm}",
                    end=" ",
                )

                try:
                    resp = s3_client.get_bucket_location(Bucket=b.Name)
                except Exception as e:
                    print(f"[WARN] Could not get bucket location => {e}")
                else:
                    b.Region = resp["LocationConstraint"]
                    print(b.Region)


if __name__ == "__main__":
    s3 = boto3.client("s3", region_name="eu-west-1")
    resp = s3.list_buckets()
    print("Getting buckets...")
    buckets: list[Bucket] = [Bucket(**item) for item in resp["Buckets"]]

    # The following function adds bucketencr info to the bucketlist class
    print("Getting bucket encryption details...")
    get_bucket_encryption_and_location(s3, buckets)

    print(" ")
    print(f"The number of CDH buckets is:     {get_nr_of_cdh_buckets(buckets)}")
    print(f"The number of CDH log buckets is: {get_nr_of_cdhlog_buckets(buckets)}")

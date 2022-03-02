import json
import pydantic
import boto3
from typing import List, Optional


class Tag(pydantic.BaseModel):
    Value: str
    Key: str


class ServerSideEncryptionByDefault(pydantic.BaseModel):
    SSEAlgorithm: str
    KMSMasterKeyID: Optional[str] = None


class ServerSideEncryptionRule(pydantic.BaseModel):
    BucketKeyEnabled: Optional[bool] = None
    ServerSideEncryptionByDefault: Optional[ServerSideEncryptionByDefault] = None


class BucketEncryption(pydantic.BaseModel):
    ServerSideEncryptionConfiguration: List[ServerSideEncryptionRule]


class Bucket(pydantic.BaseModel):
    BucketName: Optional[str] = None
    BucketEncryption: Optional[BucketEncryption] = None
    CreationDate: Optional[str]
    Tags: Optional[List[Tag]] = None

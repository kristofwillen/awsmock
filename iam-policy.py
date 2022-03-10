import json
import pydantic
import boto3
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Extra


class IAMPolicy(BaseModel):
    class Config:
        extra = Extra.forbid

    Arn: str
    AttachmentCount: int
    CreateDate: datetime
    DefaultVersionId: str
    Id: Optional[str]
    IsAttachable: Optional[bool]
    Groups: Optional[List[str]]
    Path: Optional[str]
    PermissionsBoundaryUsageCount: Optional[int]
    PolicyDocument: Optional[Dict[str, Any]]
    PolicyId: str
    PolicyName: str
    Roles: Optional[List[str]]
    UpdateDate: Optional[datetime]
    Users: Optional[List[str]]


def filter_policy(policies: List[IAMPolicy], key, value) -> List[IAMPolicy]:
    return list(filter(lambda x: x.__getattribute__(key) == value, policies))


def startswith_policy(policies: List[IAMPolicy], key, value) -> List[IAMPolicy]:
    return list(filter(lambda x: x.__getattribute__(key).startswith(value), policies))


def get_nr_of_cdh_policies(policies: List[IAMPolicy]) -> int:
    return len(startswith_policy(policies, "PolicyName", "cdh"))


def get_nr_of_cdp_policies(policies: List[IAMPolicy]) -> int:
    return len(startswith_policy(policies, "PolicyName", "cdp"))


if __name__ == "__main__":
    nr_of_cdh_policies = 0
    nr_of_cdp_policies = 0
    nr_of_policies = 0
    policies: list[IAMPolicy] = []

    iam = boto3.client("iam", region_name="eu-west-1")
    print("Getting policies...")
    paginator = iam.get_paginator("list_policies")
    resp_iterator = paginator.paginate(
        Scope="Local", PaginationConfig={"MaxItems": 5000, "PageSize": 1000}
    )

    for page_index, page in enumerate(resp_iterator):
        policies = [IAMPolicy(**item) for item in page["Policies"]]
        print(f"Getting page {page_index} of policies...")
        nr_of_cdh_policies += get_nr_of_cdh_policies(policies)
        nr_of_cdp_policies += get_nr_of_cdp_policies(policies)
        nr_of_policies += len(page["Policies"])

    print(" ")
    print(f"Found {nr_of_policies} policies!")
    print(f"The number of CDH policies is: {nr_of_cdh_policies}")
    print(f"The number of CDP policies is: {nr_of_cdp_policies}")

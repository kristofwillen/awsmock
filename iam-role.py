import json
import pydantic
import boto3
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Extra, Field, conint, constr


class Policy(BaseModel):
    PolicyDocument: Union[str, Dict[str, Any]]
    PolicyName: str


class RoleLastUsed(BaseModel):
    LastUsedDate: datetime
    Region: str


class Tag(BaseModel):
    class Config:
        extra = Extra.forbid

    Key: str
    Value: str


class IAMRole(BaseModel):
    Arn: Optional[str]
    AssumeRolePolicyDocument: Union[Dict[str, Any], str]
    Description: Optional[str]
    CreateDate: datetime
    ManagedPolicyArns: Optional[List[str]]
    MaxSessionDuration: Optional[int]
    Path: Optional[str]
    PermissionsBoundary: Optional[str]
    Policies: Optional[List[Policy]]
    RoleId: Optional[str]
    RoleName: Optional[str]
    RoleLastUsed: Optional[RoleLastUsed]
    Tags: Optional[List[Tag]]


def filter_role(roles: List[IAMRole], key, value) -> List[IAMRole]:
    return list(filter(lambda x: x.__getattribute__(key) == value, roles))


def startswith_roles(roles: List[IAMRole], key, value) -> List[IAMRole]:
    return list(filter(lambda x: x.__getattribute__(key).startswith(value), roles))


def get_nr_of_cdh_roles(roles: List[IAMRole]) -> int:
    return len(startswith_roles(roles, "RoleName", "cdh"))


def get_nr_of_cdp_roles(roles: List[IAMRole]) -> int:
    return len(startswith_roles(roles, "RoleName", "cdp"))


if __name__ == "__main__":

    nr_of_cdh_roles = 0
    nr_of_cdp_roles = 0
    roles: list[IAMRole] = []

    iam = boto3.client("iam", region_name="eu-west-1")
    print("Getting roles...")
    paginator = iam.get_paginator("list_roles")
    resp_iterator = paginator.paginate(
        PaginationConfig={"MaxItems": 1000, "PageSize": 1000}
    )

    for page_index, page in enumerate(resp_iterator):
        print(f"Found {len(page['Roles'])} roles")
        roles = [IAMRole(**item) for item in page["Roles"]]
        print(f"Getting page {page_index} of roles...")
        nr_of_cdh_roles += get_nr_of_cdh_roles(roles)
        nr_of_cdp_roles += get_nr_of_cdp_roles(roles)

    print(" ")
    print(f"Found {len(roles)} roles!")
    print(f"The number of CDH roles is: {nr_of_cdh_roles}")
    print(f"The number of CDP roles is: {nr_of_cdp_roles}")

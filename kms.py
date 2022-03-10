from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Extra, Field, conint, constr


class KeyUsage(Enum):
    ENCRYPT_DECRYPT = "ENCRYPT_DECRYPT"
    SIGN_VERIFY = "SIGN_VERIFY"


class KeySpec(Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RSA_4096 = "RSA_4096"
    ECC_NIST_P256 = "ECC_NIST_P256"
    ECC_NIST_P384 = "ECC_NIST_P384"
    ECC_NIST_P521 = "ECC_NIST_P521"
    ECC_SECG_P256K1 = "ECC_SECG_P256K1"


class Tag(BaseModel):
    Key: str
    Value: str


class KmsKey(BaseModel):
    Description: Optional[str] = None
    Enabled: Optional[bool]
    EnableKeyRotation: Optional[bool]
    KeyPolicy: Union[Dict[str, Any], str]
    KeyUsage: Optional[KeyUsage]
    KeySpec: Optional[KeySpec]
    MultiRegion: Optional[bool]
    PendingWindowInDays: Optional[int]
    Tags: Optional[List[Tag]]
    Arn: Optional[str]
    KeyId: str

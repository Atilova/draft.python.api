from enum import StrEnum, auto
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from src.identity.enum import (
    JWKKeyType,
    JWKKeyUse,
    RSAJWKKeyAlgorithm,
)


type _IdentityPermission = list[str]


class RSAJWKPublicKey(BaseModel):
    kid: UUID
    kty: Literal[JWKKeyType.RSA] = JWKKeyType.RSA
    use: JWKKeyUse
    alg: RSAJWKKeyAlgorithm
    n: str
    e: str


class RSAJWKPrivateKey(BaseModel):
    kid: UUID
    kty: Literal[JWKKeyType.RSA] = JWKKeyType.RSA
    use: JWKKeyUse
    alg: RSAJWKKeyAlgorithm
    n: str
    e: str
    d: str
    p: str
    q: str
    dp: str
    dq: str
    qi: str


class IdentityKeyCreate(BaseModel):
    name: str
    permissions: _IdentityPermission


class IdentityKeyCreateResult(BaseModel):
    name: str
    key: RSAJWKPrivateKey
    permissions: _IdentityPermission


class IdentityKeyDelete(BaseModel):
    kid: UUID


class IdentityKeySetPermissions(BaseModel):
    kid: UUID
    permissions: _IdentityPermission


class IdentityJWTSign(BaseModel):
    class _Extra(BaseModel): ...

    type: JWKKeyType
    key: RSAJWKPrivateKey
    # extra: _Extra


class IdentityJWTValidate(BaseModel):
    token: str


class IdentityJWTStatus(StrEnum):
    VALID = auto()
    INVALID = auto()
    EXPIRED = auto()


class IdentityJWTValidateResult(BaseModel):
    status: IdentityJWTStatus

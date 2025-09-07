from typing import NamedTuple, Protocol, Self
from uuid import uuid4

from src.draftpythonapi.exceptions import BusinessError
from src.identity.enum import (
    JWKKeyType,
    JWKKeyUse,
    RSAJWKKeyAlgorithm,
)


class RSAJWKPublicKey(NamedTuple):
    kid: str
    kty: JWKKeyType
    alg: RSAJWKKeyAlgorithm
    use: JWKKeyUse
    n: str
    e: str

    @classmethod
    def from_dict(cls, value: dict) -> Self:
        return RSAJWKPublicKey(
            kid=value["kid"],
            kty=value["kty"],
            alg=value["alg"],
            use=value["use"],
            n=value["n"],
            e=value["e"],
        )


class RSAJWKPrivateKey(NamedTuple):
    kid: str
    kty: JWKKeyType
    alg: RSAJWKKeyAlgorithm
    use: JWKKeyUse
    n: str
    e: str
    d: str
    p: str
    q: str
    dp: str
    dq: str
    qi: str

    @classmethod
    def from_dict(cls, value: dict) -> Self:
        return RSAJWKPrivateKey(
            kid=value["kid"],
            kty=value["kty"],
            alg=value["alg"],
            use=value["use"],
            n=value["n"],
            e=value["e"],
            d=value["d"],
            p=value["p"],
            q=value["q"],
            dp=value["dp"],
            dq=value["dq"],
            qi=value["qi"],
        )


class JWKS[PublicKey, PrivateKey](NamedTuple):
    public_key: PublicKey
    private_key: PrivateKey


class IdentityKeyAlreadyExistsError(BusinessError): ...
class IdentityKeyInvalidNameError(BusinessError): ...
class IdentityKeyInvalidPermissionsError(BusinessError): ...


class IdentityKey[PublicKey]:
    __slots__ = (
        "_name",
        "_permissions",
        "_public_key",
    )

    def __init__(
        self,
        *,
        name: str,
        public_key: PublicKey,
        permissions: list[str],
    ):
        self._name = name
        self._public_key = public_key
        self._permissions = permissions

    def matches_permissions(self, expected_permission: str): ...

    def set_permissions(self, permissions: list[str]): ...

    @property
    def name(self):
        return self._name

    @property
    def permissions(self):
        return self._permissions


class IRepository(Protocol):
    async def exists(self, name: str) -> bool: ...


class IGenerateJWKS[PublicKey, PrivateKey](Protocol):
    def __call__(self, kid: str) -> JWKS[PublicKey, PrivateKey]: ...


class IdentityKeyService:
    def __init__(self, repository: IRepository):
        self._repository = repository

    async def create[PublicKey, PrivateKey](
        self,
        *,
        name: str,
        permissions: list[str],
        generate_jwks: IGenerateJWKS[PublicKey, PrivateKey],
    ) -> tuple[IdentityKey[PublicKey], PrivateKey]:
        # TODO: validate name
        # TODO: validate permission

        if await self._repository.exists(name):
            raise IdentityKeyAlreadyExistsError(
                f"Identity key with name: '{name}' already exists."
            )

        kid = str(uuid4())
        jwks = generate_jwks(kid)
        identity_key = IdentityKey[PublicKey](
            name=name,
            permissions=permissions,
            public_key=jwks.public_key,
        )

        return identity_key, jwks.private_key

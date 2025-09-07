
from typing import Protocol

from src.identity.domain import (
    IdentityKeyService,
    JWKS as dom_JWKS,
    RSAJWKPrivateKey as dom_RSAJWKPrivateKey,
    RSAJWKPublicKey as dom_RSAJWKPublicKey
)
from src.identity.dto import (
    IdentityKeyCreate,
    IdentityKeyCreateResult,
    IdentityKeyDelete,
    IdentityKeySetPermissions,
    RSAJWKPrivateKey,
)
from src.identity.repository import IdentityRepository


class IJWKSService(Protocol):
    def generate_rsa_jwks(
        self, kid: str
    ) -> dom_JWKS[dom_RSAJWKPublicKey, dom_RSAJWKPrivateKey]: ...


class IdentityKeyCreateUseCase:
    __slots__ = (
        "_identity_repository",
        "_jwks_service",
    )

    def __init__(
        self,
        *,
        jwks_service: IJWKSService,
        identity_repository: IdentityRepository,
    ):
        self._jwks_service = jwks_service
        self._identity_repository = identity_repository

    async def __call__(self, dto: IdentityKeyCreate) -> IdentityKeyCreateResult:
        domain_service = IdentityKeyService(self._identity_repository)
        
        identity_key, private_key = await domain_service.create(
            name=dto.name,
            permissions=dto.permissions,
            generate_jwks=self._jwks_service.generate_rsa_jwks
        )

        self._identity_repository.save(identity_key)

        return IdentityKeyCreateResult(
            name=identity_key.name,
            key=RSAJWKPrivateKey(
                kid=private_key.kid,
                use=private_key.use,
                alg=private_key.alg,
                n=private_key.n,
                e=private_key.e,
                d=private_key.d,
                p=private_key.p,
                q=private_key.q,
                dp=private_key.dp,
                dq=private_key.dq,
                qi=private_key.qi,
            ),
            permissions=identity_key.permissions,
        )


class IdentityKeyDeleteUseCase:
    def __init__(self): ...

    async def __call__(self, dto: IdentityKeyDelete) -> None:
        print("IdentityKeyDeleteUseCase: ", dto)


class IdentityKeySetPermissionsUseCase:
    def __init__(self): ...

    async def __call__(self, dto: IdentityKeySetPermissions) -> None:
        print("IdentityKeySetPermissionsUseCase: ", dto)

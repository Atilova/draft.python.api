from typing import Protocol

from injector import Module, provider, singleton

from src.identity.dto import (
    IdentityKeyCreate,
    IdentityKeyCreateResult,
    IdentityKeyDelete,
    IdentityKeySetPermissions,
)
from src.identity.enum import RSAJWKKeyAlgorithm
from src.identity.jwks import JWKSService, JWKSServiceConfig
from src.identity.repository import IdentityRepository
from src.identity.usecase import (
    IdentityKeyCreateUseCase,
    IdentityKeyDeleteUseCase,
    IdentityKeySetPermissionsUseCase,
)


class IUseCase[DTO, ResultDTO](Protocol):
    def __call__(self, dto: DTO) -> ResultDTO: ...


type IKeyCreateUseCase = IUseCase[IdentityKeyCreate, IdentityKeyCreateResult]
type IKeyDeleteUseCase = IUseCase[IdentityKeyDelete, None]
type IKeySetPermissionsUseCase = IUseCase[IdentityKeySetPermissions, None]


class IdentityDIContainer(Module):
    def __init__(self):
        super().__init__()

        self._jwks_service = JWKSService(
            config=JWKSServiceConfig(
                rsa_key_algorithm=RSAJWKKeyAlgorithm.RS256,
            )
        )
        self._execute_key_create_use_case = IdentityKeyCreateUseCase(
            jwks_service=self._jwks_service,
            identity_repository=IdentityRepository(),
        )
        self._execute_key_delete_use_case = IdentityKeyDeleteUseCase()
        self._execute_key_set_permissions_use_case = IdentityKeySetPermissionsUseCase()

    @provider
    @singleton
    def provide_key_create_use_case(self) -> IKeyCreateUseCase:
        return self._execute_key_create_use_case

    @provider
    @singleton
    def provide_key_delete_use_case(self) -> IKeyDeleteUseCase:
        return self._execute_key_delete_use_case

    @provider
    @singleton
    def provide_key_set_permissions_use_case(self) -> IKeySetPermissionsUseCase:
        return self._execute_key_set_permissions_use_case

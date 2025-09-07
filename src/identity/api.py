from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi_injector import Injected, attach_injector
from injector import Injector

from src.identity.di import (
    IdentityDIContainer,
    IKeyCreateUseCase,
    IKeyDeleteUseCase,
    IKeySetPermissionsUseCase,
)
from src.identity.dto import (
    IdentityKeyCreate,
    IdentityKeyCreateResult,
    IdentityKeyDelete,
    IdentityKeySetPermissions,
)


def lifespan(app: FastAPI):
    attach_injector(app, Injector([IdentityDIContainer()]))

    yield


router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
    lifespan=lifespan,
)


@router.post("/key/create/")
async def key_create(
    request: IdentityKeyCreate,
    key_create: IKeyCreateUseCase = Injected(IKeyCreateUseCase),
) -> IdentityKeyCreateResult:
    return await key_create(request)


@router.post("/key/delete/")
async def key_delete(
    request: IdentityKeyDelete,
    key_delete: IKeyDeleteUseCase = Injected(IKeyDeleteUseCase),
) -> None:
    return await key_delete(request)


@router.post("/key/setPermissions/")
async def key_set_permissions(
    request: IdentityKeySetPermissions,
    key_set_permissions: IKeySetPermissionsUseCase = Injected(IKeySetPermissionsUseCase),
) -> None:
    return await key_set_permissions(request)

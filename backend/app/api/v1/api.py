from fastapi import APIRouter
from .workflows import router as workflows_router
from .node_types import router as node_types_router
from .execution import router as execution_router

api_router = APIRouter()

api_router.include_router(
    workflows_router,
    tags=["workflows"]
)

api_router.include_router(
    node_types_router,
    tags=["node-types"]
)

api_router.include_router(
    execution_router,
    tags=["execution"]
)

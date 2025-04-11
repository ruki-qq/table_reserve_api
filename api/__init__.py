from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from api.v1.views import table_router, reservation_router

http_bearer = HTTPBearer(auto_error=False)

router_v1 = APIRouter(dependencies=[Depends(http_bearer)])
router_v1.include_router(table_router)
router_v1.include_router(reservation_router)

import httpx
from fastapi import APIRouter,Request,Response
from app.config import settings
from app.middleware.rbac import verify_and_inject

router=APIRouter(prefix="/api/forests",tags=["Partiels"])

async def _proxy(path: str, request: Request, payload: dict | None) -> Response:
    body = await request.body()
    headers = {
        "Content-Type": request.headers.get("Content-Type", "application/json"),
        "Authorization": request.headers.get("Authorization", ""),
    }
    async with httpx.AsyncClient(base_url=settings.FOREST_SERVICE_URL) as client:
        resp = await client.request(
            method=request.method,
            url=f"/forests{path}",
            content=body,
            headers=headers,
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )

@router.api_route("/{forest_id}/partiels",methods=["GET","POST"])
async def partiels_root(forest_id:int,request:Request):
    payload=await verify_and_inject(request)
    return await _proxy(f"/{forest_id}/partiels",request,payload)

@router.api_route("/{forest_id}/partiels/{partiel_id}",methods=["GET", "PUT", "DELETE"])
async def partiel_by_id(forest_id:int,partiel_id:int,request:Request):
    payload=await verify_and_inject(request)
    return await _proxy(f"/{forest_id}/partiels/{partiel_id}",request,payload)
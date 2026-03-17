from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.partiel_schema import PartielUpdate,PartielCreate,PartielResponse
from app.services import partiel_service
from app.utils.deps import require_permission

router=APIRouter(prefix="/forests/{forest_id}/partiels",tags=["partiels"])

@router.get("",response_model=list[PartielResponse])
async def list_partiels(forest_id:int,db:AsyncSession=Depends(get_db),_=Depends(require_permission("partiel:read"))):
    return await partiel_service.get_partiels(forest_id,db)

@router.post("",response_model=PartielResponse,status_code=201)
async def create_partiel(forest_id:int,data:PartielCreate,db:AsyncSession=Depends(get_db),_=Depends(require_permission("partiel:create"))):
    return await partiel_service.create_partiel(forest_id,data,db)

@router.get("/{partiel_id}",response_model=PartielResponse)
async def get_partiel(partiel_id:int,paritel_id,db:AsyncSession=Depends(get_db),_=Depends(require_permission("partiel:read"))):
    return await partiel_service.get_partiel(partiel_id,db)

@router.put("/{partiel_id}",response_model=PartielResponse)
async def update_partiel(forest_id:int,partiel_id:int,data:PartielUpdate,db:AsyncSession=Depends(get_db),_=Depends(require_permission("partiel:update"))):
    return await partiel_service.update_partiel(partiel_id,data,db)

@router.delete("/{partiel_id}",status_code=204)
async def delete_partiel(forest_id:int,partiel_id:int,db:AsyncSession=Depends(get_db),_=Depends(require_permission("partiel:delete"))):
    await partiel_service.delete_partiel(partiel_id,db)
    
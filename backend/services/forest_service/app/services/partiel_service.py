import json,shapely
from fastapi import HTTPException,status
from geoalchemy2.shape import from_shape,to_shape
from shapely.geometry import mapping
from sqlalchemy import select,text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.partiel import Partiel
from app.schemas.partiel_schema import PartielCreate,PartielResponse,PartielUpdate

def _geojson_to_wkb_polygon(geojson:dict):
    if geojson["type"]!="Polygon":
        raise ValueError(f"Expected Polygon, got {geojson['type']}")
    geom=shapely.from_geojson(json.dumps(geojson))
    return from_shape(geom,srid=4326)

def _to_response(p:Partiel)-> PartielResponse:
    return PartielResponse(
        id=p.id,
        forest_id=p.forest_id,
        name=p.name,
        description=p.description,
        area_hectares=p.area_hectars,
        boundary_geojson=mapping(to_shape(p.boundary)),
        created_at=p.created_at,
        updated_at=p.updated_at
    )

async def create_partiel(forest_id:int,data:PartielCreate,db:AsyncSession)->PartielResponse:
    p=Partiel(forest_id=forest_id,name=data.name,description=data.description,boundary=_geojson_to_wkb_polygon(data.boundary_geojson))
    db.add(p)
    await db.flush()
    area=await db.execute(
        text("SELECT ST_Area(boundary::geography)/10000 FROM partiels WHERE id=:id"), {"id": p.id}
    )
    p.area_hectars=area.scalar()
    await db.commit()
    await db.refresh(p)
    return _to_response(p)

async def get_partiels(forest_id:int,db:AsyncSession)->list[PartielResponse]:
    result=await db.execute(select(Partiel).where(Partiel.forest_id==forest_id))
    return[_to_response(p) for p in result.scalars().all()]


async def update_partiel(partiel_id:int,data:PartielUpdate,db:AsyncSession)->PartielResponse:
    result=await db.execute(select(Partiel).where(Partiel.id==partiel_id))
    p=result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Partiel Not Found")
    if data.name:p.name=data.name
    if data.description:p.description=data.description
    if data.boundary_geojson:
        p.boundary=_geojson_to_wkb_polygon(data.boundary_geojson)
        await db.flush()
        area=await db.execute(
            text("SELECT ST_Area(boundary::geography)/10000 FROM partiels WHERE id=:id"), {"id": p.id}
        )
        p.area_hectars=area.scalar()
    await db.commit()
    await db.refresh(p)
    return _to_response(p)

async def delete_partiel(partiel_id:int,db:AsyncSession):
    result=await db.execute(select(Partiel).where(Partiel.id==partiel_id))
    p=result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Partiel Not Found")
    await db.delete(p)
    await db.commit()

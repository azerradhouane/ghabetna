from datetime import datetime
from pydantic import BaseModel

class PartielCreate(BaseModel):
    name:str
    description:str|None=None
    boundary_geojson:dict

class PartielUpdate(BaseModel):
    name:str|None=None
    description:str|None=None
    boundary_geojson:dict|None=None

class PartielResponse(BaseModel):
    id:int
    forest_id:int
    name:str
    description: str|None
    area_hectares:float|None
    boundary_geojson: dict
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes=True
from datetime import datetime
from typing import Any
from geoalchemy2 import Geometry
from sqlalchemy import String,Text,Float,func
from sqlalchemy.orm import Mapped,mapped_column
from app.database import Base

class Forest(Base):
    __tablename__="forests"

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(200),unique=True,nullable=False)
    region:Mapped[str|None]=mapped_column(String(200),nullable=True)
    description:Mapped[str|None]=mapped_column(Text,nullable=True)

    boundary:Mapped[Any]=mapped_column(
        Geometry("MULTIPOLYGON",srid=4326,spatial_index=True),nullable=True
    )
    center_point:Mapped[Any]=mapped_column(
        Geometry("POINT",srid=4326,spatial_index=True),nullable=True
    )
    area_hectars:Mapped[float|None]=mapped_column(Float,nullable=True)

    created_at:Mapped[datetime]=mapped_column(default=func.now(),server_default=func.now())
    updated_at:Mapped[datetime]=mapped_column(default=func.now(),server_default=func.now(),onupdate=func.now())

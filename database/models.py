from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from database import BaseModel


class Param(BaseModel):
    __tablename__ = "params"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    en_name = Column(String(255), nullable=False)


class ArtifactParam(BaseModel):
    __tablename__ = "artifact_params"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    artifact_id = Column(ForeignKey("artifacts.id"))
    param_id = Column(ForeignKey("params.id"))
    max = Column(Float(), nullable=False)
    min = Column(Float(), nullable=False)
    name_color = Column(String(255), nullable=False)
    value_color = Column(String(255), nullable=False)

    artifact = relationship("Artifact", back_populates="artifact_params")
    param = relationship("Param", back_populates="artifact_params")

    __table_args__ = (UniqueConstraint('artifact_id', 'param_id', name='_artifact_param_uc'),)


class Artifact(BaseModel):
    __tablename__ = "artifacts"

    id = Column(String(15), primary_key=True, index=True)
    name = Column(String(63), nullable=False)
    en_name = Column(String(63), nullable=False)
    description = Column(String(1023))
    en_description = Column(String(1023))
    category = Column(String(63), nullable=False)
    en_category = Column(String(63), nullable=False)
    weight = Column(Float, nullable=False)


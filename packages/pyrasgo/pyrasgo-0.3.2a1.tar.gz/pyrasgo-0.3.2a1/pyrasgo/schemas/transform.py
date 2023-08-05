from datetime import date, datetime
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, TypeVar, Union


class TransformBase(BaseModel):
    name: str
    sourceCode: str


class Transform(TransformBase):
    id: int
    name: str
    sourceCode: str
    arguments: Optional[List]


# POST Transform
class TransformCreate(TransformBase):
    name: str
    sourceCode: str


# Utilities
class TransformUtilityDefinition(BaseModel):
    name: str
    description: str
    arguments: Dict[str, str]


class TransformUtility(BaseModel):
    name: str
    arguments: Dict[str, str]
    resultArgumentName: str


class TransformArgs(BaseModel):
    """
    Schema/contract for Executing a Transform
    """
    transformId: int
    arguments: Dict[str, str]
    utilities: Optional[List[TransformUtility]]


class TransformExecute(BaseModel):
    """
    Contract for execution of one or more transforms
    """
    dataSourceId: int
    newSourceName: Optional[str]
    transformArgs: List[TransformArgs]


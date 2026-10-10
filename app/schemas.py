from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    published: bool = True


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    published: bool

    class Config:
        from_attributes = True

class TaskAtulizacao(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

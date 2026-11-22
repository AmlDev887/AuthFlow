from pydantic import BaseModel,Field
from schemas import enums
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    title: str | None = None
    status: enums.TaskStatus | None = None
    created_at: datetime | None = None

class TaskFilter(BaseModel):
    title: str | None = None
    status: enums.TaskStatus | None = None
    filter: str = "title"
    sort: enums.TaskSort = enums.TaskSort.DESC
    date_from:datetime
    date_to:datetime

from fastapi import APIRouter, HTTPException, status, Query
from app.database.db import DBconnection
from app.schemas import task
from typing import Annotated, List
from app.models.models import Task
from sqlalchemy import select
from app.schemas import enums

router = APIRouter(prefix="/task",
                   tags=["task"])


@router.get("/task_search",response_model=List[task.TaskResponse])
async def search_task(search: Annotated[task.TaskFilter, Query()],
                      db:DBconnection,
                      skip: int = Query(default = 0, ge = 0),
                      limit: int = Query(default = 20, ge = 5, le=20)):
    """Поиск тасков"""
    
    stmt = select(Task)
    if search.title is not None:
        safe = search.title.replace("\\", "\\\\").replace("%", r"%").replace("_", r"\_")
        stmt = stmt.where(Task.title.ilike(f"%{safe}%"), escape = "\\")

    if search.status is not None:
        stmt = stmt.where(Task.status == search.status)

    if search.date_from is not None:
        stmt = stmt.where(Task.created_at >= search.date_from)

    if search.date_to is not None:
        stmt = stmt.where(Task.created_at <= search.date_to)
    
    if search.sort is not None:
        if search.sort == enums.TaskSort.DESC:
            stmt = stmt.order_by(Task.created_at.desc())

        if search.sort == enums.TaskSort.ASC:
            stmt = stmt.order_by(Task.created_at.asc())

    result = await db.execute(stmt.offset(skip).limit(limit))
    answer = result.scalars().all()

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Ничего не нашли по запросу"
        )

    return answer
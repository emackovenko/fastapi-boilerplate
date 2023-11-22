from typing import List, Optional


from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    results: List[dict] = Field(
        ..., description="Результаты выборки из API", example=[{"id": 1}, {"id": 2}]
    )
    count: int = Field(
        ...,
        description="Количество результатов",
    )
    next_page_url: Optional[str] = Field(
        ...,
        description="URL следующей страницы, если такая существует",
    )
    previous_page_url: Optional[str] = Field(
        ...,
        description="URL последней страницы, если существует",
    )

    class Config:
        orm_mode = True

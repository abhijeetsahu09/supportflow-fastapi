
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=100
    )

    description: str = Field(
        min_length=10,
        max_length=2000
    )


class TicketPublic(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    model_config = {"from_attributes": True}

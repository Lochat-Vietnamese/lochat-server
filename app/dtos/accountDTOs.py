from uuid import UUID
from pydantic import Field
from app.dtos.baseDTO import BaseDTO


class GetAccountByIdDTO(BaseDTO):
    account_id: UUID = Field(
        title="Account ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
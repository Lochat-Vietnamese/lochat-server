from uuid import UUID
from pydantic import Field
from app.dtos.baseDTO import BaseDTO


class GetConversationByIdDTO(BaseDTO):
    conversation_id: UUID = Field(
        title="Conversation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )

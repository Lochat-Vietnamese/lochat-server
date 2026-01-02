from uuid import UUID
from pydantic import Field, field_validator
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetMessageByIdDTO(BaseDTO):
    message_id: UUID = Field(
        title="Message ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    is_active: bool | None = Field(
        title="Message Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
class GetMessageByConversationDTO(BaseDTO):
    conversation_id: UUID = Field(
        title="Conversation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    page: int = Field(
        title="Current Page",
        ge=1,
        default=1, 
        examples=1
    )
    page_size: int = Field(
        title="Page Size",
        ge=5,
        lt=100,
        default=10, 
        examples=20
    )
    is_active: bool | None = Field(
        title="Messages Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
class GetLastMessageDTO(BaseDTO):
    conversation_id: UUID = Field(
        title="Conversation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
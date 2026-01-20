from typing import Optional
from uuid import UUID
from pydantic import Field, field_validator
from app.enums.messageTypes import MessageTypes
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetMessageByIdDTO(BaseDTO):
    message_id: UUID = Field(
        title="Message ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    
# TODO: thêm yêu cầu kiểm tra đối với tài khoản đang đăng nhập (phân quyền)
class SearchMessagesDTO(BaseDTO):
    conversation_id: UUID = Field(
        title="Conversation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    get_last: bool | None = Field(
        title="Get Last Message",
        default=None, 
        examples=True
    )
    sender_id: UUID | None = Field(
        title="Message Sender ID",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    type: Optional[str] | None = Field(
        title="message type",
        default=None,
        examples="text"
    )
    content: str | None = Field(
        title="message content",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    media_id: UUID | None = Field(
        title="message media id",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    reply: UUID | None = Field(
        title="replying to message id",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
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
    
    @field_validator("hometown")
    @classmethod
    def validate_message_type(cls, value: str | None):
        if value is None:
            return value
        if value not in MessageTypes.values:
            raise ValueError("Invalid message type")
        return value
    
    @classmethod
    def is_only_pagination(self):
        pagination_fields = {"page", "page_size", "is_active"}

        for field_name, value in self.model_dump().items():
            if field_name not in pagination_fields and value is not None:
                return False
        return True

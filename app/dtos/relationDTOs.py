from typing import Optional
from uuid import UUID
from pydantic import Field, field_validator
from app.dtos.profileDTOs import GetProfileByIdDTO
from app.enums.relationStatus import RelationStatus
from app.enums.relationTypes import RelationTypes
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetRelationByIdDTO(BaseDTO):
    relation_id: UUID = Field(
        title="Relation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    
class SearchRelationsDTO(BaseDTO):
    user_id: UUID | None = Field(
        title="User ID",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    type: Optional[str] | None = Field(
        title="relation type",
        default=None,
        examples="FRIEND"
    )
    first_user_id: UUID | None = Field(
        title="First ID of user in relation",
        default=None,
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    second_user_id: UUID | None = Field(
        title="Second ID of user in relation",
        default=None,
        examples="223e4567-e89b-12d3-a456-426655440000"
    )
    status: Optional[str] | None = Field(
        title="Relation Status",
        default=None,
        examples="ACCEPTED"
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
        examples=10
    )
    is_active: bool | None = Field(
        title="Relation Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
    @field_validator("type", mode="before")
    @classmethod
    def validate_relation_type(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationTypes.values:
            raise ValueError("Invalid relation type")
        return value
   
    @field_validator("status", mode="before")
    @classmethod
    def validate_relation_status(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationStatus.values:
            raise ValueError("Invalid relation status")
        return value
    
    @classmethod
    def is_only_pagination(self):
        pagination_fields = {"page", "page_size", "is_active"}

        for field_name, value in self.model_dump().items():
            if field_name not in pagination_fields and value is not None:
                return False
        return True
    
class CreateRelationDTO(BaseDTO):
    type: Optional[str] | None = Field(
        title="relation type",
        default=None,
        examples="FRIEND"
    )
    first_user_id: UUID = Field(
        title="First ID of user in relation",
        examples="123e4567-e89b-12d3-a456-426655440000"
    )
    second_user_id: UUID = Field(
        title="Second ID of user in relation",
        examples="223e4567-e89b-12d3-a456-426655440000"
    )
    status: Optional[str] | None = Field(
        title="Relation Status",
        default=None,
        examples="ACCEPTED"
    )

    @field_validator("type", mode="before")
    @classmethod
    def validate_relation_type(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationTypes.values:
            raise ValueError("Invalid relation type")
        return value
   
    @field_validator("status", mode="before")
    @classmethod
    def validate_relation_status(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationStatus.values:
            raise ValueError("Invalid relation status")
        return value
    
class UpdateRelationDTO(BaseDTO):
    id: UUID = Field(
        title="Relation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
        alias="relation_id"
    )
    type: Optional[str] | None = Field(
        title="relation type",
        default=None,
        examples="FRIEND"
    )
    status: Optional[str] | None = Field(
        title="Relation Status",
        default=None,
        examples="ACCEPTED"
    )
    is_active: bool | None = Field(
        title="Relation Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
    @field_validator("type", mode="before")
    @classmethod
    def validate_relation_type(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationTypes.values:
            raise ValueError("Invalid relation type")
        return value
   
    @field_validator("status", mode="before")
    @classmethod
    def validate_relation_status(cls, value: str | None):
        if value is None:
            return value
        if value not in RelationStatus.values:
            raise ValueError("Invalid relation status")
        return value
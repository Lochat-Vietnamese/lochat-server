from uuid import UUID
from pydantic import Field, field_validator
from app.dtos.profileDTOs import GetProfileByIdDTO
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetRelationByIdDTO(BaseDTO):
    relation_id: UUID = Field(
        title="Relation ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    is_active: bool | None = Field(
        title="Relation Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)

class GetRelationByProfilesDTO(BaseDTO):
    first_profile_id: UUID = Field(
        title="Profile ID 1",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    second_profile_id: UUID = Field(
        title="Profile ID 2",
        example="123e4567-e89b-12d3-a456-426655440000",
    )
    is_active: bool | None = Field(
        title="Relation Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
class GetRelationByProfileDTO(BaseDTO):
    profile: GetProfileByIdDTO = Field(
        title="Profile ID",
    )
    is_active: bool | None = Field(
        title="Relation Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
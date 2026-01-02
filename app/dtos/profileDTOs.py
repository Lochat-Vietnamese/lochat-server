from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import Field, field_validator
from app.enums.provinces import Provinces
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class GetAllProfileDTO(BaseDTO):
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
        title="Profiles Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)

class GetProfileByIdDTO(BaseDTO):
    profile_id: UUID = Field(
        title="Profile ID",
        example="123e4567-e89b-12d3-a456-426655440000",
    ),
    is_active: bool | None = Field(
        title="Profile Activity Status",
        default=None, 
        examples=True
    )

    @field_validator("is_active", mode="before")
    def parse_is_active(cls, input):
        return ParseBool(input)
    
class CreateProfileDTO(BaseDTO):
    nickname: str = Field(
        title="Nickname",
        example="Jenix",
    )
    phone_number: str = Field(
        title="Phone Number",
        example="1234567890",
    )
    dob: date = Field(
        title="Date of Birth",
        example="2000-01-01",
    )
    bio: str | None = Field(
        title="bio",
        examples="profile bio",
        default=None,
    )
    avatar_url: str | None = Field(
        title="avatar url",
        examples="https://example.com/avatar.jpg",
        default=None,
    )
    address: str | None = Field(
        title="address",
        examples="example address",
        default=None,
    )
    hometown: Optional[str] | None = Field(
        title="hometown",
        examples="Ho Chi Minh City",
        default=None,
    )
    education: str | None = Field(
        title="education",
        examples="university",
        default=None,
    )
    work: str | None = Field(
        title="work",
        examples="developer",
        default=None,
    )
    hobbies: str | None = Field(
        title="hobbies",
        examples="playing game",
        default=None,
    )
    
    @field_validator("dob")
    @classmethod
    def validate_min_age(cls, value: date):
        today = date.today()
        if value > today:
            raise ValueError("Date of birth cannot be in the future")
        
        age = (today.year - value.year - ((today.month, today.day) < (value.month, value.day)))

        if age < 14:
            raise ValueError("User must be at least 14 years old")
        return value
    
    @field_validator("hometown")
    @classmethod
    def validate_hometown(cls, value: str | None):
        if value is None:
            return value
        if value not in Provinces.values:
            raise ValueError("Invalid hometown")
        return value
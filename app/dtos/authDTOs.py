from datetime import date
from typing import Optional
from pydantic import Field, field_validator, EmailStr
from app.enums.provinces import Provinces
from app.enums.responseMessages import ResponseMessages
from app.utils.parseBool import ParseBool
from app.dtos.baseDTO import BaseDTO


class SignInDTO(BaseDTO):
    username: str | None = Field(
        title="username",
        example="example",
        default=None,
    )
    email: EmailStr | None = Field(
        title="email",
        examples="example@email.com",
        default=None,
    )
    password: str = Field(
        title="password",
        examples="12345678",
        min_length=8,
    )

class SignUpDTO(BaseDTO):
    username: str = Field(
        title="username",
        example="example",
        min_length=3,
    )
    email: EmailStr = Field(
        title="email",
        examples="example@email.com",
    )
    password: str = Field(
        title="password",
        examples="12345678",
        min_length=8,
    )
    nickname: str = Field(
        title="nickname",
        examples="nickname",
        min_length=3,
    )
    dob: date = Field(
        title="date of birth",
        examples="2000-01-01",
    )
    phone_number: str = Field(
        title="phone number",
        examples="0123456789",
        min_length=10,
        max_length=10,
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

    @field_validator("hometown")
    def validate_hometown(cls, input: str):
        if input and input not in Provinces.choices:
            raise ValueError(ResponseMessages.INVALID_INPUT)
        return input
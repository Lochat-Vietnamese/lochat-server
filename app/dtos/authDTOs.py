from pydantic import Field, EmailStr, model_validator
from app.dtos.profileDTOs import CreateProfileDTO
from app.dtos.baseDTO import BaseDTO
from app.utils.exceptionHelper import ExceptionHelper


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
    @model_validator(mode="after")
    def validate_username_or_email(self):
        if not self.username and not self.email:
            ExceptionHelper.throw_bad_request(
                "Phải cung cấp username hoặc email"
            )
        return self

class SignUpDTO(BaseDTO):
    username: str = Field(
        title="Username",
        example="username",
        min_length=5,
        max_length=20,
        regex="^[a-zA-Z0-9]+$"
    )
    password: str = Field(
        title="Password",
        example="password",
        min_length=8,
        max_length=30,
        regex="^\S+$"
    )
    email: EmailStr = Field(
        title="Email",
        example="email"
    )
    profile: CreateProfileDTO = Field(
        title="Profile",
    )
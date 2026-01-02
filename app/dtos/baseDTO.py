from pydantic import BaseModel, ConfigDict, ValidationError
from app.utils.exceptionHelper import ExceptionHelper

class BaseDTO(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
    )

    @classmethod
    def validate_or_throw(cls, data):
        try:
            return cls.model_validate(data)
        except ValidationError as e:
            errors = e.errors()

            lines = []
            for err in errors:
                loc_path = ".".join(str(loc) for loc in err["loc"])
                msg = err["msg"]
                lines.append(f"{loc_path}: {msg}")

            messages = "\n".join(lines)

            ExceptionHelper.throw_bad_request(messages)
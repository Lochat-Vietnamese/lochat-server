from typing import TypedDict


class CookieOptions(TypedDict, total=False):
    value: str
    max_age: int
    httponly: bool
    secure: bool
    samesite: str
    path: str
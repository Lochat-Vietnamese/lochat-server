from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper


class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.publicEndpoint = getattr(settings, "PUBLIC_ENDPOINTS", [])

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.publicEndpoint):
            return self.get_response(request)

        rawAccessToken = request.COOKIES.get("access_token")
            
        if not rawAccessToken:
            return BaseResponse.error(status_code=HttpStatus.UNAUTHORIZED, code=ResponseCodes.INVALID_TOKEN, message="Missing access token", details="Missing access token")

        try:
            access_token = AccessToken(rawAccessToken)
            user_id = access_token.get("user_id")
            profile_id = access_token.get("profile_id")
            if not user_id or not profile_id:
                return BaseResponse.error(status_code=HttpStatus.UNAUTHORIZED, code=ResponseCodes.INVALID_TOKEN, message="Invalid token", details="Invalid token")

            request.user_id = user_id
            request.logging_in_profile = profile_id
            request.access_token = rawAccessToken
        except (TokenError, InvalidToken):
            return BaseResponse.error(status_code=HttpStatus.UNAUTHORIZED, code=ResponseCodes.INVALID_TOKEN, message="Invalid token", details="Invalid token")

        return self.get_response(request)
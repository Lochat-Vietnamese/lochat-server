from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from app.utils.baseResponse import BaseResponse


class JwtMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.publicEndpoint = getattr(settings, "PUBLIC_ENDPOINTS", [])

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.publicEndpoint):
            return self.get_response(request)

        requestHeader = request.headers.get("Authorization")
        rawAccessToken = None
        if requestHeader and requestHeader.startswith("Bearer "):
            rawAccessToken = requestHeader.split(" ")[1]
        else:
            rawAccessToken = request.COOKIES.get("access_token")
            
        if not rawAccessToken:    
            return BaseResponse.error(message="missing_token")

        try:
            token = AccessToken(rawAccessToken)
            user_id = token.get("user_id")
            if not user_id:
                return BaseResponse.error(message="invalid_token")

            request.user_id = user_id
        except (TokenError, InvalidToken):
            return BaseResponse.error(message="expired_token")

        return self.get_response(request)
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
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
            ExceptionHelper.throw_unauthorized(message="Missing access token")

        try:
            access_token = AccessToken(rawAccessToken)
            user_id = access_token.get("user_id")
            if not user_id:
                ExceptionHelper.throw_unauthorized(message="Invalid token")

            request.logging_in_account = user_id
            request.access_token = rawAccessToken
        except (TokenError, InvalidToken):
            ExceptionHelper.throw_unauthorized(message="Invalid token")

        return self.get_response(request)
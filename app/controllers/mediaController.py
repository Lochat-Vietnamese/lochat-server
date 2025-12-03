from django.views import View

from app.enums.responseMessages import ResponseMessages
from app.mapping.mediaMapping import MediaMapping
from app.services.mediaService import MediaService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.parseBool import ParseBool
from app.utils.requestData import RequestData


class MediaController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                media_id = data.get("media_id")
                is_active = ParseBool(data.get("is_active", "true"))
                if media_id:
                    result = MediaService.get_by_id(
                        media_id=media_id, is_active=is_active
                    )
                    return BaseResponse.send(data=MediaMapping(result).data)
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            if action == "upload":
                files = data.get("files")
                if files:
                    result = await MediaService.storage_media_file(data=data)
                    return BaseResponse.send(
                        data=MediaMapping(result, many=True).data
                    )
                ExceptionHelper.throw_bad_request(ResponseMessages.MISSING_DATA)

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

from django.views import View

from app.dtos.mediaDTOs import GetMediaByIdDTO, StorageMediaFilesDTO
from app.enums.responseMessages import ResponseMessages
from app.mapping.mediaMapping import MediaMapping
from app.services.mediaService import MediaService
from app.utils.baseResponse import BaseResponse
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class MediaController(View):
    async def post(self, request, action=None):
        try:
            data = RequestData(request=request)

            if action == "get-by-id":
                dto = GetMediaByIdDTO(**data)

                result = MediaService.get_by_id(dto)
                return BaseResponse.send(data=MediaMapping(result).data)

            if action == "upload":
                dto = StorageMediaFilesDTO(**data)
                result = await MediaService.storage_media_file(data=dto)
                return BaseResponse.send(
                    data=MediaMapping(result, many=True).data
                )

            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_ENDPOINT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

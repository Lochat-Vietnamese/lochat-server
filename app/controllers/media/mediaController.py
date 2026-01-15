from django.views import View

from app.dtos.mediaDTOs import GetMediaByIdDTO, StorageMediaFilesDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.mediaMapping import MediaMapping
from app.services.mediaService import MediaService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData


class MediaController(View):
    async def get(self, request, media_id=None):
        try:
            if media_id:
                media_dto = GetMediaByIdDTO(media_id=media_id)

                result = MediaService.get_by_id(media_id=media_dto.media_id)
                return BaseResponse.success(
                    data=MediaMapping(result).data,
                    code=ResponseCodes.GET_MEDIA_BY_ID_SUCCESS,
                    message="Get media by id successfully",
                )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    async def post(self, request):
        try:
            data = RequestData(request)
            storage_media_dto = StorageMediaFilesDTO(data=data)

            result = await MediaService.storage_media_file(
                files=storage_media_dto.files,
                uploader_id=storage_media_dto.uploader_id,
            )
            return BaseResponse.success(
                data=result,
                code=ResponseCodes.STORAGE_MEDIA_SUCCESS,
                message="Storage media files successfully",
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
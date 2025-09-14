from django.views import View

from app.mapping.mediaMapping import MediaMapping
from app.services.mediaService import MediaService
from app.utils.baseResponse import BaseResponse
from app.utils.logHelper import LogHelper
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
                    result = MediaService.get_by_id(media_id=media_id, is_active=is_active)
                    if result:
                        return BaseResponse.success(data=MediaMapping(result).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
                
            if action == "upload":
                files = data.get('files')
                if files:
                    result = await MediaService.storage_media_file(data=data)
                    if result:
                        return BaseResponse.success(data=MediaMapping(result, many=True).data)
                    return BaseResponse.error(message="process_failed")
                return BaseResponse.error()
            

            return BaseResponse.error(message="invalid_endpoint")
        except Exception as e:
            LogHelper.error(message=str(e))
            return BaseResponse.internal(data=str(e))
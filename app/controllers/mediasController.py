# from rest_framework.views import APIView
# from app.mapping.mediasMapping import MediasMapping
# from app.utils.baseResponse import BaseResponse
# from app.services.mediasService import MediasService
# import json

# class MediasController(APIView):
#     def post(self, request, action):
#         try:
#             if action and action == "upload":
#                 file = request.FILES.get('file')
#                 metadata_from_request = request.data.get("metadata")

#                 if not file:
#                     return BaseResponse.error("Không tìm thấy file")
                
#                 try:
#                     metadata = json.loads(metadata_from_request) if metadata_from_request else {}
#                 except Exception:
#                     return BaseResponse.error("Metadata không phải JSON hợp lệ")

#                 result = MediasService.storage_media_file(file, metadata)
#                 if result:
#                     return BaseResponse.success(data=result)
#                 return BaseResponse.error("upload thất bại")
            
#             if action and action == "get-by-id":
#                 media_id = request.data.get("media_id")
#                 result = MediasService.find_by_id(media_id=media_id)
#                 if result:
#                     return BaseResponse.success(data=MediasMapping(result).data)

#             return BaseResponse.internal()
#         except Exception as e:
#             return BaseResponse.internal(message=str(e))
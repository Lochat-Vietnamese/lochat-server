# import uuid
# from typing import Dict
# from django.utils.timezone import datetime, now
# from app.repositories.mediasRepo import MediasRepo
# from app.services.accountsService import AccountsService
# from app.enums.mediaTypes import MediaTypes
# import boto3
# from django.conf import settings


# class MediasService:
#     @staticmethod
#     def storage_media_file(file: bytes, metadata: dict):
#         try:
#             file_name = file.name
#             file_type = file.content_type
#             file_size = file.size
#             conversation_id = metadata.get("conversation_id")

#             if not file or not file_name or not file_type or file_name == "" or file_type == "":
#                 return None
            
#             storage_client = boto3.client(
#                 's3',
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                 region_name=settings.AWS_S3_REGION_NAME
#             )
            
#             file_extension = file_name.split('.')[-1]
#             storage_key = f"{uuid.uuid4()}.{file_extension}"

#             if file_extension in ["png", "jpg", "jpeg", "webp", "bmp"]:
#                 file_type = "photo"
#             elif file_extension in ["mp3", "wav", "ogg", "m4a"]:
#                 file_type = "audio"
#             elif file_extension in ["mp4", "mov", "avi", "mkv"]:
#                 file_type = "video"
#             elif file_extension in ["gif"]:
#                 file_type = "gif"
#             elif file_extension in ["pdf"]:
#                 file_type = "pdf"

#             match file_type:
#                 case "audio":
#                     folder = "audio"
#                 case "photo":
#                     folder = "photo"
#                 case "video":
#                     folder = "video"
#                 case "gif":
#                     folder = "gif"
#                 case "pdf":
#                     folder = "pdf"
#                 case _:
#                     folder = "unknow"

#             storage_url = f"{folder}/{conversation_id}/{storage_key}"
            
#             storage_client.upload_fileobj(
#                 file,
#                 settings.AWS_STORAGE_BUCKET_NAME,
#                 storage_url,
#                 ExtraArgs={
#                     'ACL': settings.AWS_DEFAULT_ACL,
#                     'ContentType': file_type
#                 }
#             )
                        
#             return {
#                 'file_name': file_name,
#                 'file_type': file_type,
#                 'file_size': file_size,
#                 'file_url': storage_url
#             }
#         except Exception:
#             return None
        
#     @staticmethod
#     def is_valid_media_type(media_type: str):
#         return media_type in MediaTypes.values

#     @staticmethod
#     def find_all():
#         try:
#             return MediasRepo.get_all()
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_id(media_id: str):
#         try:
#             if media_id and str(media_id).strip():
#                 uuid_obj = uuid.UUID(media_id)
#                 return MediasRepo.get_by_id(uuid_obj)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_uploader(account_id: str):
#         try:
#             if account_id and str(account_id).strip():
#                 account = AccountsService.find_by_id(account_id)
#                 if account:
#                     return MediasRepo.filter_by_uploader(account)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_type(media_type: str):
#         try:
#             if media_type and str(media_type).strip() and MediasService.is_valid_media_type(media_type):
#                 return MediasRepo.filter_by_type(media_type)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_name(name: str):
#         try:
#             if name and str(name).strip():
#                 return MediasRepo.filter_by_name(name)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_size(size: int):
#         try:
#             if size and size > 0:
#                 return MediasRepo.filter_by_size(size)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_duration(duration: int):
#         try:
#             if duration and duration > 0:
#                 return MediasRepo.filter_by_duration(duration)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_key(key: str):
#         try:
#             if key and str(key).strip():
#                 return MediasRepo.filter_by_key(key)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_date_created(date: datetime = None):
#         try:
#             return MediasRepo.filter_by_date_created(date or now())
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_status(status: bool = True):
#         try:
#             return MediasRepo.filter_by_status(status)
#         except Exception:
#             return None

#     @staticmethod
#     def find_by_birth_day(date: datetime):
#         try:
#             if date:
#                 return MediasRepo.filter_by_birth_day(date)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def create(data: Dict):
#         try:
#             uploader_id = data.get("uploader_id")
#             name = data.get("name")
#             type = data.get("type")
#             size = data.get("size")
#             url = data.get("url")

#             if not all([uploader_id, name, type, size, url]):
#                 return None

#             existing = MediasRepo.get_by_url(url)
#             if existing and existing.exists():
#                 return None

#             return MediasRepo.do_create(data)
#         except Exception:
#             return None

#     @staticmethod
#     def update(media_id: str, data: Dict):
#         try:
#             if media_id and str(media_id).strip() and any(data.values()):
#                 media = MediasService.find_by_id(media_id)
#                 if not media:
#                     return None
#                 return MediasRepo.do_update(media, data)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def delete(media_id: str):
#         try:
#             if media_id and str(media_id).strip():
#                 media = MediasService.find_by_id(media_id)
#                 if not media:
#                     return None
#                 return MediasRepo.do_delete(media)
#             return None
#         except Exception:
#             return None

#     @staticmethod
#     def hard_delete(media_id: str):
#         try:
#             if media_id and str(media_id).strip():
#                 media = MediasService.find_by_id(media_id)
#                 if not media:
#                     return False
#                 return MediasRepo.do_hard_delete(media)
#             return False
#         except Exception:
#             return False
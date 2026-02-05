from typing import Dict, List
import uuid
from uuid import UUID
from django.forms import Media
from django.core.files.uploadedfile import UploadedFile
from app.repositories.mediaRepo import MediaRepo
from app.enums.mediaTypes import MediaTypes
import aioboto3
from django.conf import settings

from app.services.profileConversationService import ProfileConversationService
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class MediaService:
    @staticmethod
    def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return MediaRepo.all(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_id(media_id: UUID, is_active: bool | None = True):
        try:
            return MediaRepo.find_by_id(media_id=UUID(media_id), is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_url(url: str, is_active: bool | None = True):
        try:
            if url and str(url).strip():
                return MediaRepo.find_by_url(url=url, is_active=is_active)
            ExceptionHelper.throw_bad_request("Invalid url")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def create(data: Dict):
        try:
            name = data.get("name")
            type = data.get("type")
            size = data.get("size")
            url = data.get("url")

            if not all([name, type, size, url]):
                ExceptionHelper.throw_bad_request("Missing required fields")

            existing = MediaService.get_by_url(url=url, is_active=None)
            if existing:
                ExceptionHelper.throw_bad_request("Media already exists")

            return MediaRepo.handle_create(FieldsFilter(data=data, entity=Media))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update(data: Dict):
        try:
            media_id = data.get("id")
            if media_id and str(media_id).strip():
                media = MediaService.get_by_id(media_id=media_id, is_active=None)
                
                return MediaRepo.handle_update(media, FieldsFilter(data=data, entity=Media))
            ExceptionHelper.throw_bad_request("Invalid media id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def delete(media_id: UUID):
        try:
            if media_id and str(media_id).strip():
                media = MediaService.get_by_id(media_id, is_active=None)
               
                return MediaRepo.handle_delete(media)
            ExceptionHelper.throw_bad_request("Invalid media id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def hard_delete(media_id: UUID):
        try:
            if media_id and str(media_id).strip():
                media = MediaService.get_by_id(media_id, is_active=None)
               
                return MediaRepo.handle_hard_delete(media)
            ExceptionHelper.throw_bad_request("Invalid media id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
         
    @staticmethod
    def storage_media_file(files: List[UploadedFile], uploader_id: UUID):
        try:
            uploader = ProfileConversationService.get_by_id(profileConversation_id=uploader_id, is_active=None)

            session = aioboto3.Session()
            result = []

            with session.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            ) as storage_client:
            
                for file in files:
                    file_name = file.name
                    content_type = file.content_type
                    file_size = file.size

                    
                    file_extension = file_name.split('.')[-1].lower()
                    storage_key = f"{uuid.uuid4()}.{file_extension}"

                    if file_extension in ["png", "jpg", "jpeg", "webp", "bmp"]:
                        file_type = "photo"
                    elif file_extension in ["mp3", "wav", "ogg", "m4a"]:
                        file_type = "audio"
                    elif file_extension in ["mp4", "mov", "avi", "mkv"]:
                        file_type = "video"
                    elif file_extension in ["gif"]:
                        file_type = "gif"
                    elif file_extension in ["pdf"]:
                        file_type = "pdf"

                    match file_type:
                        case "audio":
                            folder = "audio"
                        case "photo":
                            folder = "photo"
                        case "video":
                            folder = "video"
                        case "gif":
                            folder = "gif"
                        case "pdf":
                            folder = "pdf"
                        case _:
                            folder = "unknow"

                    storage_url = f"{folder}/{uploader.conversation.id}/{storage_key}"
                    
                    storage_client.upload_fileobj(
                        file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        storage_url,
                        ExtraArgs={
                            'ACL': settings.AWS_DEFAULT_ACL,
                            'ContentType': content_type
                        }
                    )
                    media = MediaService.create({
                        "uploader": uploader,
                        "name": file_name,
                        "type": file_type,
                        "size": file_size,
                        "url": storage_url,
                    })

                    result.append(media)
            return result
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
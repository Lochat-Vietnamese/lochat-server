import uuid
from typing import Dict
from django.forms import Media
from app.dtos.mediaDTOs import GetMediaByIdDTO, StorageMediaFilesDTO
from app.enums.responseMessages import ResponseMessages
from app.repositories.mediaRepo import MediaRepo
from app.enums.mediaTypes import MediaTypes
import aioboto3
from django.conf import settings
from asgiref.sync import sync_to_async

from app.services.profileConversationService import ProfileConversationService
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class MediaService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            return await sync_to_async(MediaRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_id(dto: GetMediaByIdDTO):
        try:
            return await sync_to_async(MediaRepo.find_by_id)(media_id=dto.media_id, is_active=dto.is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_uploader(profile_conversation_id: str, page: int = 1, page_size: int = 20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            if profile_conversation_id and str(profile_conversation_id).strip():
                profileConversation = await ProfileConversationService.get_by_id(profile_conversation_id, is_active)
                return await sync_to_async(MediaRepo.find_by_uploader)(uploader=profileConversation, page=page, page_size=page_size, is_active=is_active)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_type(media_type: str, page: int = 1, page_size: int = 20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            if media_type and str(media_type).strip():
                return await sync_to_async(MediaRepo.find_by_type)(MediaTypes(media_type), page=page, page_size=page_size, is_active=is_active)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
        
    @staticmethod
    async def get_by_url(url: str, is_active: bool | None = True):
        try:
            if url and str(url).strip():
                return await sync_to_async(MediaRepo.find_by_url)(url=url, is_active=is_active)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def create(data: Dict):
        try:
            name = data.get("name")
            type = data.get("type")
            size = data.get("size")
            url = data.get("url")

            if not all([name, type, size, url]):
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            existing = await MediaService.get_by_url(url=url, is_active=None)
            if existing:
                ExceptionHelper.throw_bad_request(ResponseMessages.ALREADY_EXISTS)

            return MediaRepo.handle_create(FieldsFilter(data=data, entity=Media))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update(data: Dict):
        try:
            media_id = data.get("id")
            if media_id and str(media_id).strip():
                media = await MediaService.get_by_id(media_id=media_id, is_active=None)
                
                return await sync_to_async(MediaRepo.handle_update)(media, FieldsFilter(data=data, entity=Media))
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def delete(media_id: str):
        try:
            if media_id and str(media_id).strip():
                media = await MediaService.get_by_id(media_id, is_active=None)
               
                return await sync_to_async(MediaRepo.handle_delete)(media)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def hard_delete(media_id: str):
        try:
            if media_id and str(media_id).strip():
                media = await MediaService.get_by_id(media_id, is_active=None)
               
                return await sync_to_async(MediaRepo.handle_hard_delete)(media)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
         
    @staticmethod
    async def storage_media_file(dto: StorageMediaFilesDTO):
        try:
            uploader = await ProfileConversationService.get_by_id(profileConversation_id=dto.uploader_id, is_active=None)

            files = dto.files
            session = aioboto3.Session()
            result = []

            async with session.client(
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
                    
                    await storage_client.upload_fileobj(
                        file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        storage_url,
                        ExtraArgs={
                            'ACL': settings.AWS_DEFAULT_ACL,
                            'ContentType': content_type
                        }
                    )
                    media = await MediaService.create({
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
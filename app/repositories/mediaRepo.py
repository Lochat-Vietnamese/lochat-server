import uuid
from app.entities.media import Media
from app.entities.profileConversation import ProfileConversation
from app.enums.mediaTypes import MediaTypes
from django.core.paginator import Paginator

from app.enums.responseMessages import ResponseMessages
from app.utils.exceptionHelper import ExceptionHelper

class MediaRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Media.objects.select_related("uploader").all().order_by("-created_at")
            else:
                queryset = Media.objects.select_related("uploader").filter(is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception as e:
            raise e
    
    @staticmethod
    def find_by_id(media_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Media.objects.select_related("uploader").get(id=media_id)
            return Media.objects.select_related("uploader").get(id=media_id, is_active=is_active)
        except Media.DoesNotExist:
             ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_url(url: str, is_active: bool | None):
        try:
            if is_active is None:
                return Media.objects.select_related("uploader").get(url=url)
            return Media.objects.select_related("uploader").get(url=url, is_active=is_active)
        except Media.DoesNotExist:
             ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_uploader(uploader: ProfileConversation, is_active: bool | None):
        try:
            if is_active is None:
                return Media.objects.select_related("uploader").get(uploader=uploader)
            return Media.objects.select_related("uploader").get(uploader=uploader, is_active=is_active)
        except Media.DoesNotExist:
             ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_uploader(uploader: ProfileConversation, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Media.objects.select_related("uploader").filter(uploader=uploader).order_by("-created_at")
            else:
                queryset = Media.objects.select_related("uploader").filter(uploader=uploader, is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_type(type: MediaTypes, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Media.objects.select_related("uploader").filter(type=type).order_by("-created_at")
            else:
                queryset = Media.objects.select_related("uploader").filter(type=type, is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_name(name: str, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Media.objects.select_related("uploader").filter(name=name).order_by("-created_at")
            else:
                queryset = Media.objects.select_related("uploader").filter(name=name, is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception as e:
            raise e
  
    @staticmethod
    def handle_create(data: dict):
        try:
            return Media.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(media: Media, data: dict):
        try:
            for field, value in data.items():
                setattr(media, field, value)
            media.save(update_fields=list(data.keys()))
            return media
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(media: Media):
        try:
            media.is_active = False
            media.save(update_fields=["is_active"])
            return media
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(media: Media):
        try:
            media.delete()
            return True
        except Exception as e:
            raise e
# import uuid
# from django.utils.timezone import datetime, now
# from app.entities.medias import Medias
# from app.entities.account import Accounts
# from app.enums.mediaTypes import MediaTypes
# from django.db.models import Q


# class MediasRepo:
#     @staticmethod
#     def get_all():
#         try:
#             return Medias.objects.all()
#         except Exception:
#             return None


#     @staticmethod
#     def get_by_id(media_id: uuid.UUID):
#         try:
#             return Medias.objects.get(id=media_id)
#         except Exception:
#             return None
        
#     @staticmethod
#     def get_by_url(media_url: str):
#         try:
#             return Medias.objects.get(url=media_url)
#         except Exception:
#             return None
            
#     @staticmethod
#     def filter_by_uploader(uploader: Accounts):
#         try:
#             return Medias.objects.get(uploader=uploader)
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_type(type: MediaTypes.choices):
#         try:
#             return Medias.objects.filter(media_type=type)
#         except Exception:
#             return None
        
#     @staticmethod
#     def filter_by_name(name: str):
#         try:
#             return Medias.objects.filter(name__icontains=name)
#         except Exception:
#             return None
        
#     @staticmethod
#     def filter_by_size(size: int):
#         try:
#             return Medias.objects.filter(size__lte=size)
#         except Exception:
#             return None
        
#     @staticmethod
#     def filter_by_duration(duration: int):
#         try:
#             return Medias.objects.filter(Q(media_type=MediaTypes.VIDEO) | Q(media_type=MediaTypes.AUDIO), duration__lte=duration)
#         except Exception:
#             return None
        
#     @staticmethod
#     def filter_by_date_created(date: datetime):
#         try:
#             return Medias.objects.filter(created_at=date)
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_status(status: bool = True):
#         try:
#             return Medias.objects.filter(is_active=status)
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_birth_day(date: datetime):
#         try:
#             return Medias.objects.filter(birth = date)
#         except Exception:
#             return None

#     @staticmethod
#     def do_create(data: dict):
#         try:
#             return Medias.objects.create(**data)
#         except Exception:
#             return None

#     @staticmethod
#     def do_update(media: Medias, data: dict):
#         try:
#             for field, value in data.items():
#                 setattr(media, field, value)
#             media.updated_at = now()
#             media.save(update_fields=data.keys()) 
#             return media
#         except Exception:
#             return None

#     @staticmethod
#     def do_delete(media: Medias):
#         try:
#             media.is_active = False
#             media.updated_at = now()
#             media.save()
#             return media
#         except Exception:
#             return None

#     @staticmethod
#     def do_hard_delete(media: Medias):
#         try:
#             media.delete()
#             return True
#         except Exception:
#             return False

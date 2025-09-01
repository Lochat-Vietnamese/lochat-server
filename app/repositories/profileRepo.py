import uuid
from django.core.paginator import Paginator
from app.entities.profile import Profile


class ProfileRepo:

    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Profile.objects.all().order_by("-created_at")
            else:
                queryset = Profile.objects.filter(is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception:
            return None

    @staticmethod
    def find_by_id(profile_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Profile.objects.get(id=profile_id)
            return Profile.objects.get(id=profile_id, is_active=is_active)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def find_by_nickname(nickname: str, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Profile.objects.filter(
                    nickname__icontains=nickname
                ).order_by("nickname")
            else:
                queryset = Profile.objects.filter(
                    nickname__icontains=nickname, is_active=is_active
                ).order_by("nickname")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception:
            return None

    @staticmethod
    def find_by_phone_number(phone_number: str, is_active: bool | None):
        try:
            if is_active is None:
                return Profile.objects.get(phone_number=phone_number)
            return Profile.objects.get(phone_number=phone_number, is_active=is_active)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def handle_create(data: dict):
        try:
            return Profile.objects.create(**data)
        except Exception:
            return None

    @staticmethod
    def handle_update(profile: Profile, data: dict):
        try:
            for field, value in data.items():
                setattr(profile, field, value)
            profile.save(update_fields=list(data.keys()))
            return profile
        except Exception:
            return None

    @staticmethod
    def handle_delete(profile: Profile):
        try:
            profile.is_active = False
            profile.save(update_fields=["is_active"])
            return profile
        except Exception:
            return None

    @staticmethod
    def handle_hard_delete(profile: Profile):
        try:
            profile.delete()
            return True
        except Exception:
            return None

    @staticmethod
    async def check_exist_by_nickname(nickname: str):
        try:
            return Profile.objects.filter(nickname=nickname).exists()
        except Exception:
            return None
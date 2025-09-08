from profile import Profile
import uuid
from typing import Dict
from asgiref.sync import sync_to_async

from app.repositories.profileRepo import ProfileRepo
from app.utils.fieldsFilter import FieldsFilter


class ProfileService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                return None
            return await sync_to_async(ProfileRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_id(profile_id: str, is_active: bool | None = True):
        try:
            if profile_id and str(profile_id).strip():
                uuid_obj = uuid.UUID(profile_id)
                return await sync_to_async(ProfileRepo.find_by_id)(uuid_obj, is_active)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_nickname(
        nickname: str, page=1, page_size=20, is_active: bool | None = True
    ):
        try:
            if not nickname or page <= 0 or page_size <= 0:
                return None
            return await sync_to_async(ProfileRepo.find_by_nickname)(
                nickname, page, page_size, is_active
            )
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_phone_number(phone_number: str, is_active: bool | None = True):
        try:
            if phone_number and str(phone_number).strip():
                return await sync_to_async(ProfileRepo.find_by_phone_number)(
                    phone_number=phone_number, is_active=is_active
                )
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def create(data: Dict):
        try:
            phone_number = str(data.get("phone_number"))
            nickname = str(data.get("nickname"))
            dob = data.get("dob")
            if not all([phone_number, nickname, dob]) or await ProfileService.get_by_phone_number(phone_number=phone_number, is_active=None):
                return None
            return await sync_to_async(ProfileRepo.handle_create)(FieldsFilter(data=data, entity=Profile))
        except Exception as e:
            raise e

    @staticmethod
    async def update(data: Dict):
        try:
            profile_id = data.get("id")
            if profile_id and str(profile_id).strip() and any(data.values()):
                profile = await ProfileService.get_by_id(profile_id, None)
                if not profile:
                    return None
                return await sync_to_async(ProfileRepo.handle_update)(profile, FieldsFilter(data=data, entity=Profile))
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def delete(profile_id: str):
        try:
            if profile_id and str(profile_id).strip():
                profile = await ProfileService.get_by_id(profile_id, None)
                if not profile:
                    return None
                return await sync_to_async(ProfileRepo.handle_delete)(profile)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def hard_delete(profile_id: str):
        try:
            if profile_id and str(profile_id).strip():
                profile = await ProfileService.get_by_id(profile_id, None)
                if not profile:
                    return None
                return await sync_to_async(ProfileRepo.handle_hard_delete)(profile)
            return None
        except Exception as e:
            raise e
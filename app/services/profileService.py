from app.entities.profile import Profile
from typing import Dict

from app.repositories.profileRepo import ProfileRepo
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class ProfileService:
    @staticmethod
    def get_all(page: int = 1, page_size: int = 20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return ProfileRepo.all(page=page, page_size=page_size, is_active=True)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_id(profile_id: str, is_active: bool | None = True):
        try:
            return ProfileRepo.find_by_id(profile_id=profile_id, is_active= is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_phone_number(phone_number: str, is_active: bool | None = True):
        try:
            if phone_number and str(phone_number).strip():
                return ProfileRepo.find_by_phone_number(
                    phone_number=phone_number, is_active=is_active
                )
            ExceptionHelper.throw_bad_request("Missing phone number")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def create(data: Dict):
        try:
            phone_number = str(data.get("phone_number"))
            nickname = str(data.get("nickname"))
            dob = data.get("dob")
            if not all([phone_number, nickname, dob]) or ProfileService.get_by_phone_number(phone_number=phone_number, is_active=None):
                ExceptionHelper.throw_bad_request("Missing required fields")
            return ProfileRepo.handle_create(FieldsFilter(data=data, entity=Profile))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update(data: Dict):
        try:
            profile_id = data.get("id")
            if profile_id and str(profile_id).strip() and any(data.values()):
                profile = ProfileService.get_by_id(profile_id, None)
               
                return ProfileRepo.handle_update(profile, FieldsFilter(data=data, entity=Profile))
            ExceptionHelper.throw_bad_request("Missing required fields")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def delete(profile_id: str):
        try:
            if profile_id and str(profile_id).strip():
                profile = ProfileService.get_by_id(profile_id, None)
 
                return ProfileRepo.handle_delete(profile)
            ExceptionHelper.throw_bad_request("Missing required fields")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def hard_delete(profile_id: str):
        try:
            if profile_id and str(profile_id).strip():
                profile = ProfileService.get_by_id(profile_id, None)
         
                return ProfileRepo.handle_hard_delete(profile)
            ExceptionHelper.throw_bad_request("Missing required fields")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def search_profiles(search_data: Dict):
        try:
            page = search_data.pop("page")
            page_size = search_data.pop("page_size")
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return ProfileRepo.handle_search_profiles(search_data=search_data, page=page, page_size=page_size)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
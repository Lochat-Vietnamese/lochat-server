import uuid
from typing import Dict
from app.entities.profileConversation import ProfileConversation
from app.enums.conversationTypes import ConversationTypes
from app.repositories.profileConversationRepo import ProfileConversationRepo
from app.services.accountService import AccountService
from app.services.profileService import ProfileService
from app.services.conversationService import ConversationService

from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class ProfileConversationService:
    @staticmethod
    def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            return ProfileConversationRepo.all(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_id(profileConversation_id: str, is_active: bool | None = True):
        try:
            if profileConversation_id and str(profileConversation_id).strip():
                uuid_obj = uuid.UUID(profileConversation_id)
                return ProfileConversationRepo.find_by_id(
                    profileConversation_id=uuid_obj, is_active=is_active
                )
            ExceptionHelper.throw_bad_request("Invalid profileConversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_profile(
        profile_id: str,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = True,
    ):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            profile = ProfileService.get_by_id(profile_id=profile_id)

            if not profile:
                ExceptionHelper.throw_bad_request("Invalid profile id")
                
            return ProfileConversationRepo.find_by_profile(
                profile=profile,
                page=page,
                page_size=page_size,
                is_active=is_active,
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_conversation(
        conversation_id: str,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = True,
    ):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationService.get_by_id(conversation_id)
                return ProfileConversationRepo.find_by_conversation(
                    conversation=conversation,
                    page=page,
                    page_size=page_size,
                    is_active=is_active,
                )
            ExceptionHelper.throw_bad_request("Invalid conversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def create(data: Dict):
        try:
            profile_id = data.get("profile_id")
            conversation_id = data.get("conversation_id")
            if not (profile_id or conversation_id) or not (
                str(profile_id).strip() or str(conversation_id).strip()
            ):
                ExceptionHelper.throw_bad_request("Missing required fields")

            profile = ProfileService.get_by_id(
                profile_id=profile_id, is_active=True
            )
            conversation = ConversationService.get_by_id(
                conversation_id=conversation_id, is_active=True
            )

            data["profile"] = profile
            data["conversation"] = conversation
            if not data.get("conversation_name"):
                data["conversation_name"] = profile.nickname
            return ProfileConversationRepo.handle_create(
                FieldsFilter(data=data, entity=ProfileConversation)
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update(data: Dict):
        try:
            profileConversation_id = data.get("id")
            if (
                profileConversation_id
                and str(profileConversation_id).strip()
                and any(data.values())
            ):
                ProfileConversationService.get_by_id(
                    profileConversation_id=profileConversation_id, is_active=None
                )
                return ProfileConversationRepo.handle_update(
                    ProfileConversation,
                    FieldsFilter(data=data, entity=ProfileConversation),
                )
            ExceptionHelper.throw_bad_request("Invalid profileConversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def delete(profileConversation_id: str):
        try:
            if profileConversation_id and str(profileConversation_id).strip():
                profileConversation = ProfileConversationService.get_by_id(
                    profileConversation_id=profileConversation_id, is_active=None
                )

                return ProfileConversationRepo.handle_delete(
                    profileConversation
                )
            ExceptionHelper.throw_bad_request("Invalid profileConversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def hard_delete(accontConversation_id: str):
        try:
            if accontConversation_id and str(accontConversation_id).strip():
                profileConversation = ProfileConversationService.get_by_id(
                    profileConversation_id=accontConversation_id, is_active=None
                )

                return ProfileConversationRepo.handle_hard_delete(
                    ProfileConversation=profileConversation
                )
            ExceptionHelper.throw_bad_request("Invalid profileConversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_common_conversations(
        profile1_id: str,
        profile2_id: str,
        is_active: bool | None,
        type: ConversationTypes | None,
    ):
        try:
            prof1 = ProfileService.get_by_id(profile_id=profile1_id)
            prof2 = ProfileService.get_by_id(profile_id=profile2_id)
            return ProfileConversationRepo.find_common_conversations(prof1, prof2, is_active=is_active, type=type)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_both(
        profile_id: str, conversation_id: str, is_active: bool | None = True
    ):
        try:
            if (conversation_id and profile_id) and (
                str(conversation_id).strip() and str(profile_id).strip()
            ):
                profile = ProfileService.get_by_id(profile_id)
                conversation = ConversationService.get_by_id(conversation_id)
                if profile and conversation:
                    return ProfileConversationRepo.find_by_both(
                        profile=profile, conversation=conversation, is_active=is_active
                    )
            ExceptionHelper.throw_bad_request("Invalid profile or conversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update_last_accessed(currentPC: ProfileConversation):
        try:
            return ProfileConversationRepo.handle_update_last_accessed(currentPC)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def search_memberships(search_data: Dict):
        try:
            page = search_data.pop("page")
            page_size = search_data.pop("page_size")
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return ProfileConversationRepo.handle_search_memberships(search_data=search_data, page=page, page_size=page_size)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
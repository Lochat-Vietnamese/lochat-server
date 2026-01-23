import uuid
from typing import Dict
from app.entities.profileConversation import ProfileConversation
from app.enums.conversationTypes import ConversationTypes
from app.enums.responseMessages import ResponseMessages
from app.repositories.profileConversationRepo import ProfileConversationRepo
from app.services.accountService import AccountService
from app.services.profileService import ProfileService
from app.services.conversationService import ConversationService
from asgiref.sync import sync_to_async

from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class ProfileConversationService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            return await sync_to_async(ProfileConversationRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_id(profileConversation_id: str, is_active: bool | None = True):
        try:
            if profileConversation_id and str(profileConversation_id).strip():
                uuid_obj = uuid.UUID(profileConversation_id)
                return await sync_to_async(ProfileConversationRepo.find_by_id)(
                    profileConversation_id=uuid_obj, is_active=is_active
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_account(
        account_id: str,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = True,
    ):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            if account_id and str(account_id).strip():
                account = await AccountService.get_by_id(account_id=account_id)
                profile = account.profile if account else None
                return await sync_to_async(ProfileConversationRepo.find_by_profile)(
                    profile=profile,
                    page=page,
                    page_size=page_size,
                    is_active=is_active,
                )
            ExceptionHelper.throw_bad_request("Invalid account id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_conversation(
        conversation_id: str,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = True,
    ):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            if conversation_id and str(conversation_id).strip():
                conversation = await ConversationService.get_by_id(conversation_id)
                return await sync_to_async(ProfileConversationRepo.find_by_conversation)(
                    conversation=conversation,
                    page=page,
                    page_size=page_size,
                    is_active=is_active,
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def create(data: Dict):
        try:
            profile_id = data.get("profile_id")
            conversation_id = data.get("conversation_id")
            if not (profile_id or conversation_id) or not (
                str(profile_id).strip() or str(conversation_id).strip()
            ):
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            profile = await ProfileService.get_by_id(
                profile_id=profile_id, is_active=True
            )
            conversation = await ConversationService.get_by_id(
                conversation_id=conversation_id, is_active=True
            )

            data["profile"] = profile
            data["conversation"] = conversation
            if not data.get("conversation_name"):
                data["conversation_name"] = profile.nickname
            return await sync_to_async(ProfileConversationRepo.handle_create)(
                FieldsFilter(data=data, entity=ProfileConversation)
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update(data: Dict):
        try:
            profileConversation_id = data.get("id")
            if (
                profileConversation_id
                and str(profileConversation_id).strip()
                and any(data.values())
            ):
                await ProfileConversationService.get_by_id(
                    profileConversation_id=profileConversation_id, is_active=None
                )
                return await sync_to_async(ProfileConversationRepo.handle_update)(
                    ProfileConversation,
                    FieldsFilter(data=data, entity=ProfileConversation),
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def delete(profileConversation_id: str):
        try:
            if profileConversation_id and str(profileConversation_id).strip():
                profileConversation = await ProfileConversationService.get_by_id(
                    profileConversation_id=profileConversation_id, is_active=None
                )

                return await sync_to_async(ProfileConversationRepo.handle_delete)(
                    profileConversation
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def hard_delete(accontConversation_id: str):
        try:
            if accontConversation_id and str(accontConversation_id).strip():
                profileConversation = await ProfileConversationService.get_by_id(
                    profileConversation_id=accontConversation_id, is_active=None
                )

                return await sync_to_async(ProfileConversationRepo.handle_hard_delete)(
                    ProfileConversation=profileConversation
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_common_conversations(
        acc1_id: str,
        acc2_id: str,
        is_active: bool | None,
        type: ConversationTypes | None,
    ):
        try:
            acc1 = await ProfileService.get_by_id(profile_id=acc1_id)
            acc2 = await ProfileService.get_by_id(profile_id=acc2_id)
            return await sync_to_async(
                ProfileConversationRepo.find_common_conversations
            )(acc1, acc2, is_active=is_active, type=type)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_both(
        profile_id: str, conversation_id: str, is_active: bool | None = True
    ):
        try:
            if (conversation_id and profile_id) and (
                str(conversation_id).strip() and str(profile_id).strip()
            ):
                profile = await ProfileService.get_by_id(profile_id)
                conversation = await ConversationService.get_by_id(conversation_id)
                if profile and conversation:
                    return await sync_to_async(ProfileConversationRepo.find_by_both)(
                        profile=profile, conversation=conversation, is_active=is_active
                    )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update_last_accessed(currentPC: ProfileConversation):
        try:
            return await sync_to_async(
                ProfileConversationRepo.handle_update_last_accessed
            )(currentPC)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

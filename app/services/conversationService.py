from uuid import UUID
from typing import Dict
from app.entities.conversation import Conversation
from app.repositories.conversationRepo import ConversationRepo
from app.services.profileService import ProfileService

from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class ConversationService:
    @staticmethod
    def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            return ConversationRepo.all(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_id(conversation_id: UUID, is_active: bool | None = True):
        try:
            return ConversationRepo.find_by_id(conversation_id=conversation_id, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def create(data: Dict):
        try:
            creator_id = data.get("creator_id")
            if not creator_id or not str(creator_id).strip():
                ExceptionHelper.throw_bad_request("Missing required fields")
            creator = ProfileService.get_by_id(profile_id=creator_id, is_active=True)

            data["creator"] = creator
            return ConversationRepo.handle_create(FieldsFilter(data=data, entity=Conversation))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update(data: Dict):
        try:
            conversation_id = data.get("id")
            if conversation_id and str(conversation_id).strip() and any(data.values()):
                conversation = ConversationService.get_by_id(conversation_id, None)

                return ConversationRepo.handle_update(conversation, FieldsFilter(data=data, entity=Conversation))
            ExceptionHelper.throw_bad_request("Invalid conversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def delete(conversation_id: UUID):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationService.get_by_id(conversation_id, None)
              
                return ConversationRepo.handle_delete(conversation)
            ExceptionHelper.throw_bad_request("Invalid conversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def hard_delete(conversation_id: UUID):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = ConversationService.get_by_id(conversation_id, None)
           
                return ConversationRepo.handle_hard_delete(conversation)
            ExceptionHelper.throw_bad_request("Invalid conversation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
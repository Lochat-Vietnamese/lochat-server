import uuid
from typing import Dict
from app.entities.conversation import Conversation
from app.repositories.conversationRepo import ConversationRepo
from app.services.profileService import ProfileService
from asgiref.sync import sync_to_async

from app.utils.fieldsFilter import FieldsFilter


class ConversationService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                return None
            return await sync_to_async(ConversationRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_id(conversation_id: str, is_active: bool | None = True):
        try:
            if str(conversation_id).strip():
                uuid_obj = uuid.UUID(conversation_id)
                return await sync_to_async(ConversationRepo.find_by_id)(conversation_id=uuid_obj, is_active=is_active)
            return None
        except Exception as e:
            raise e
        
    @staticmethod
    async def get_by_title(title: str, is_active: bool | None = True):
        try:
            if str(title).strip():
                return await sync_to_async(ConversationRepo.find_by_title)(title=title, is_active=is_active)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def create(data: Dict):
        try:
            creator_id = data.get("creator_id")
            if not creator_id or not str(creator_id).strip():
                return None
            creator = await ProfileService.get_by_id(profile_id=creator_id, is_active=True)

            data["creator"] = creator
            return await sync_to_async(ConversationRepo.handle_create)(FieldsFilter(data=data, entity=Conversation))
        except Exception as e:
            raise e

    @staticmethod
    async def update(data: Dict):
        try:
            conversation_id = data.get("id")
            if conversation_id and str(conversation_id).strip() and any(data.values()):
                conversation = await ConversationService.get_by_id(conversation_id, None)
                if not conversation:
                    return None
                return await sync_to_async(ConversationRepo.handle_update)(conversation, FieldsFilter(data=data, entity=Conversation))
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def delete(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = await ConversationService.get_by_id(conversation_id, None)
                if not conversation:
                    return None
                return await sync_to_async(ConversationRepo.handle_delete)(conversation)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def hard_delete(conversation_id: str):
        try:
            if conversation_id and str(conversation_id).strip():
                conversation = await ConversationService.get_by_id(conversation_id, None)
                if not conversation:
                    return None
                return await sync_to_async(ConversationRepo.handle_hard_delete)(conversation)
            return None
        except Exception as e:
            raise e
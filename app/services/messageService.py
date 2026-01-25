from mailbox import Message
import uuid
from typing import Dict
from app.repositories.messageRepo import MessageRepo
from app.services.conversationService import ConversationService
from app.services.profileConversationService import ProfileConversationService
from asgiref.sync import sync_to_async

from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter

class MessageService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            return await sync_to_async(MessageRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
    
    @staticmethod
    async def get_by_id(message_id: str, is_active: bool | None = True):
        try:
            if message_id and str(message_id).strip():
                message_id = uuid.UUID(message_id)
            return await sync_to_async(MessageRepo.find_by_id)(message_id=message_id, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
            
    @staticmethod
    async def create(data: Dict):
        try:
            conversation_id = data.get("conversation_id")
            sender_id = data.get("sender_id")

            if not all([conversation_id, sender_id]):
                ExceptionHelper.throw_bad_request("Invalid conversation id or sender id")
            
            await ConversationService.get_by_id(conversation_id, is_active=None)
            await ProfileConversationService.get_by_id(sender_id, is_active=None)

            return MessageRepo.handle_create(FieldsFilter(data=data, entity=Message))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update(data: Dict):
        try:
            message_id = data.get("id")
            if message_id and str(message_id).strip():
                message = await MessageService.get_by_id(message_id=message_id, is_active=None)
                
                return await sync_to_async(MessageRepo.handle_update)(message, FieldsFilter(data=data, entity=Message))
            ExceptionHelper.throw_bad_request("Invalid message id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def delete(message_id: str):
        try:
            if message_id and str(message_id).strip():
                message = await MessageService.get_by_id(message_id, is_active=None)
               
                return await sync_to_async(MessageRepo.handle_delete)(message)
            ExceptionHelper.throw_bad_request("Invalid message id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def hard_delete(message_id: str):
        try:
            if message_id and str(message_id).strip():
                message = await MessageService.get_by_id(message_id, is_active=None)
             
                return await sync_to_async(MessageRepo.handle_hard_delete)(message)
            ExceptionHelper.throw_bad_request("Invalid message id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_last_conversation_message(conversation_id: str):
        try:
            conversation = await ConversationService.get_by_id(conversation_id=conversation_id, is_active=None)
            
            return MessageRepo.find_last_conversation_message(conversation=conversation)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
        
    @staticmethod
    async def get_by_conversation(conversation_id: str, page: int = 1, page_size: int = 20, is_active: bool | None = True):
        try:
            conversation = await ConversationService.get_by_id(conversation_id=conversation_id, is_active=is_active)
            
            return MessageRepo.find_by_conversation(conversation=conversation, page=page, page_size=page_size, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
    
    @staticmethod
    async def search_messages(search_data: Dict):
        try:
            page = search_data.pop("page")
            page_size = search_data.pop("page_size")
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return await sync_to_async(MessageRepo.handle_search_messages)(search_data=search_data, page=page, page_size=page_size)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
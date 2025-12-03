import uuid
from app.entities.conversation import Conversation
from app.entities.profileConversation import ProfileConversation
from app.enums.messageTypes import MessageTypes
from app.entities.message import Message
from django.core.paginator import Paginator

from app.enums.responseMessages import ResponseMessages
from app.utils.exceptionHelper import ExceptionHelper


class MessageRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Message.objects.select_related("conversation", "sender", "media").all().order_by("-created_at")
            else:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(is_active=is_active).order_by("-created_at")

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
    def find_by_id(message_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Message.objects.select_related("conversation", "sender", "media").get(id=message_id)
            return Message.objects.select_related("conversation", "sender", "media").get(id=message_id, is_active=is_active)
        except Message.DoesNotExist:
             ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_sender(sender: ProfileConversation, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(sender=sender).order_by("-created_at")
            else:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(sender=sender, is_active=is_active).order_by("-created_at")

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
    def find_by_type(type: MessageTypes, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(type=type).order_by("-created_at")
            else:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(type=type, is_active=is_active).order_by("-created_at")

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
    def find_by_reply(reply: uuid.UUID, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(reply=reply).order_by("-created_at")
            else:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(reply=reply, is_active=is_active).order_by("-created_at")

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
            return Message.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(message: Message, data: dict):
        try:
            for field, value in data.items():
                setattr(message, field, value)
            message.save(update_fields=list(data.keys()))
            return message
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(message: Message):
        try:
            message.is_active = False
            message.save(update_fields=["is_active"])
            return message
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(message: Message):
        try:
            message.delete()
            return True
        except Exception as e:
            raise e
        
    @staticmethod
    def find_last_conversation_message(conversation: Conversation):
        try:
            return Message.objects.filter(conversation=conversation, is_active=True).order_by("-created_at").first()
        except Message.DoesNotExist:
             ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_conversation(conversation: Conversation, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(conversation=conversation).order_by("-created_at")
            else:
                queryset = Message.objects.select_related("conversation", "sender", "media").filter(conversation=conversation, is_active=is_active).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "pages": paginator.num_pages,
                "current": items.number,
                "content": list(items),
            }
        except Exception as e:
            raise e
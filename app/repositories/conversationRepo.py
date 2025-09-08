import uuid
from app.entities.account import Account
from app.entities.conversation import Conversation
from django.core.paginator import Paginator

from app.enums.conversationTypes import ConversationTypes


class ConversationRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Conversation.objects.select_related("creator").all().order_by("-created_at")
            else:
                queryset = Conversation.objects.select_related("creator").filter(is_active=is_active).order_by("-created_at")

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
    def find_by_id(conversation_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Conversation.objects.select_related("creator").get(id=conversation_id)
            return Conversation.objects.select_related("creator").get(id=conversation_id, is_active=is_active)
        except Conversation.DoesNotExist:
            return None
        except Exception as e:
            raise e
    
    @staticmethod
    def find_by_title(title: str, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Conversation.objects.select_related("creator").filter(title=title).order_by("-created_at")
            else:
                queryset = Conversation.objects.select_related("creator").filter(title=title, is_active=is_active).order_by("-created_at")

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
    def find_by_type(type: ConversationTypes.choices ,page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Conversation.objects.select_related("creator").filter(type=type).order_by("-created_at")
            else:
                queryset = Conversation.objects.select_related("creator").filter(type=type, is_active=is_active).order_by("-created_at")

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
    def find_by_creator(creator: Account, is_active: bool | None):
        try:
            if is_active is None:
                return Conversation.objects.select_related("creator").get(creator=creator)
            return Conversation.objects.select_related("creator").get(creator=creator, is_active=is_active)
        except Conversation.DoesNotExist:
            return None
        except Exception as e:
            raise e

    @staticmethod
    def handle_create(data: dict):
        try:
            return Conversation.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(conversation: Conversation, data: dict):
        try:
            for field, value in data.items():
                setattr(conversation, field, value)
            conversation.save(update_fields=list(data.keys()))
            return conversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(conversation: Conversation):
        try:
            conversation.is_active = False
            conversation.save(update_fields=["is_active"])
            return conversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(conversation: Conversation):
        try:
            conversation.delete()
            return True
        except Exception as e:
            raise e
import uuid
from django.utils.timezone import datetime, now
from app.entities.conversation import Conversation
from django.core.paginator import Paginator


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
        except Exception:
            return None
        
    @staticmethod
    def find_by_id(account_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Conversation.objects.select_related("creator").get(id=account_id)
            return Conversation.objects.select_related("creator").get(id=account_id, is_active=is_active)
        except Account.DoesNotExist:
            return None

    @staticmethod
    def get_by_id(conversation_id: uuid.UUID):
        try:
            return Conversation.objects.select_related("creator").get(id=conversation_id)
        except Exception:
            return None
        
    @staticmethod
    def filter_by_title(title: str):
        try:
            return Conversation.objects.select_related("creator").filter(title__icontains=title)
        except Exception:
            return None

    @staticmethod
    def get_all_personal_chats():
        try:
            return Conversation.objects.select_related("creator").filter(is_group=False, is_community=False)
        except Exception:
            return None
        
    @staticmethod
    def get_all_groups(isgroup: bool):
        try:
            return Conversation.objects.select_related("creator").filter(is_group=isgroup)
        except Exception:
            return None
        
    @staticmethod
    def get_all_communities(iscommunity: bool):
        try:
            return Conversation.objects.select_related("creator").filter(is_community=iscommunity)
        except Exception:
            return None
            
    @staticmethod
    def get_by_creator(creator: Accounts):
        try:
            return Conversation.objects.select_related("creator").get(creator=creator)
        except Exception:
            return None

    @staticmethod
    def filter_by_date_created(date: datetime):
        try:
            return Conversation.objects.select_related("creator").filter(created_at=date)
        except Exception:
            return None

    @staticmethod
    def filter_by_status(status: bool = True):
        try:
            return Conversation.objects.select_related("creator").filter(is_active=status)
        except Exception:
            return None

    @staticmethod
    def filter_by_birth_day(date: datetime):
        try:
            return Conversation.objects.select_related("creator").filter(birth = date)
        except Exception:
            return None

    @staticmethod
    def do_create(data: dict):
        try:
            return Conversation.objects.select_related("creator").create(**data)
        except Exception:
            return None

    @staticmethod
    def do_update(conversation: Conversation, data: dict):
        try:
            for field, value in data.items():
                setattr(conversation, field, value)
            conversation.updated_at = now()
            conversation.save(update_fields=data.keys()) 
            return conversation
        except Exception:
            return None

    @staticmethod
    def do_delete(conversation: Conversation):
        try:
            conversation.is_active = False
            conversation.updated_at = now()
            conversation.save()
            return conversation
        except Exception:
            return None

    @staticmethod
    def do_hard_delete(conversation: Conversation):
        try:
            conversation.delete()
            return True
        except Exception:
            return False

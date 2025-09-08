import uuid
from django.utils.timezone import now
from app.entities.accountConversation import AccountConversation
from app.entities.account import Account
from app.entities.conversation import Conversation
from django.core.paginator import Paginator


class AccountConversationRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = AccountConversation.objects.select_related("account", "conversation").all().order_by("-created_at")
            else:
                queryset = AccountConversation.objects.select_related("account", "conversation").filter(is_active=is_active).order_by("-created_at")

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
    def find_by_id(accountConversation_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return AccountConversation.objects.select_related("account", "conversation").get(id=accountConversation_id)
            return AccountConversation.objects.select_related("account", "conversation").get(id=accountConversation_id, is_active=is_active)
        except Conversation.DoesNotExist:
            return None
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_account(account: Account, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = AccountConversation.objects.select_related("account", "conversation").filter(account=account).order_by("-last_accessed")
            else:
                queryset = AccountConversation.objects.select_related("account", "conversation").filter(account=account, is_active=is_active).order_by("-last_accessed")

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
    def find_by_conversation(conversation: Conversation, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = AccountConversation.objects.select_related("account", "conversation").filter(conversation=conversation).order_by("-last_accessed")
            else:
                queryset = AccountConversation.objects.select_related("account", "conversation").filter(conversation=conversation, is_active=is_active).order_by("-last_accessed")

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
    def find_by_both(account: Account, conversation: Conversation, is_active: bool | None):
        try:
            if is_active is None:
                return AccountConversation.objects.select_related("account", "conversation").get(conversation=conversation, account=account)
            return AccountConversation.objects.select_related("account", "conversation").get(conversation=conversation, account=account, is_active=is_active)
        except Conversation.DoesNotExist:
            return None
        except Exception as e:
            raise e

    @staticmethod
    def handle_create(data: dict):
        try:
            return AccountConversation.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(accountConversation: AccountConversation, data: dict):
        try:
            for field, value in data.items():
                setattr(accountConversation, field, value)
            accountConversation.save(update_fields=list(data.keys()))
            return accountConversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(accountConversation: AccountConversation):
        try:
            accountConversation.is_active = False
            accountConversation.save(update_fields=["is_active"])
            return accountConversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(accountConversation: AccountConversation):
        try:
            accountConversation.delete()
            return True
        except Exception as e:
            raise e

    @staticmethod
    def handle_update_last_accessed(accountConversation: AccountConversation):
        try:
            accountConversation.last_accessed = now()
            accountConversation.save()
            return accountConversation
        except Exception as e:
            raise e

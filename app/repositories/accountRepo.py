import uuid
from django.core.paginator import Paginator
from app.entities.account import Account


class AccountRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Account.objects.select_related("profile").all().order_by("-created_at")
            else:
                queryset = Account.objects.select_related("profile").filter(is_active=is_active).order_by("-created_at")

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
                return Account.objects.select_related("profile").get(id=account_id)
            return Account.objects.select_related("profile").get(id=account_id, is_active=is_active)
        except Account.DoesNotExist:
            return None

    @staticmethod
    def find_by_username(username: str, is_active: bool | None):
        try:
            if is_active is None:
                return Account.objects.select_related("profile").get(username=username)
            return Account.objects.select_related("profile").get(username=username, is_active=is_active)
        except Account.DoesNotExist:
            return None

    @staticmethod
    def find_by_email(email: str, is_active: bool | None):
        try:
            if is_active is None:
                return Account.objects.select_related("profile").get(email=email)
            return Account.objects.select_related("profile").get(email=email, is_active=is_active)
        except Account.DoesNotExist:
            return None

    @staticmethod
    def handle_create(data: dict):
        try:
            return Account.objects.create(**data)
        except Exception:
            return None

    @staticmethod
    def handle_update(account: Account, data: dict):
        try:
            for field, value in data.items():
                setattr(account, field, value)
            account.save(update_fields=list(data.keys()))
            return account
        except Exception:
            return None

    @staticmethod
    def handle_delete(account: Account):
        try:
            account.is_active = False
            account.save(update_fields=["is_active"])
            return account
        except Exception:
            return None

    @staticmethod
    def handle_hard_delete(account: Account):
        try:
            account.delete()
            return True
        except Exception:
            return None

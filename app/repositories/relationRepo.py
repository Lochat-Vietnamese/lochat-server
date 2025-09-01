import uuid
from django.core.paginator import Paginator
from django.db.models import Q

from app.entities.relation import Relation
from app.entities.profile import Profile


class RelationRepo:

    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Relation.objects.all().order_by("-created_at")
            else:
                queryset = Relation.objects.filter(is_active=is_active).order_by("-created_at")

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
    def find_by_id(relation_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Relation.objects.get(id=relation_id)
            else:
                return Relation.objects.get(id=relation_id, is_active=is_active)
        except Relation.DoesNotExist:
            return None

    @staticmethod
    def find_by_both_users(user1: Profile, user2: Profile, is_active: bool | None):
        try:
            if is_active is None:
                return Relation.objects.get(
                    Q(first_user=user1, second_user=user2) |
                    Q(first_user=user2, second_user=user1)
                )
            else:
                return Relation.objects.get(
                    (Q(first_user=user1, second_user=user2) |
                     Q(first_user=user2, second_user=user1)) &
                    Q(is_active=is_active)
                )
        except Relation.DoesNotExist:
            return None

    @staticmethod
    def find_by_one_user(user: Profile, page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = Relation.objects.filter(
                    Q(first_user=user) | Q(second_user=user)
                ).order_by("-created_at")
            else:
                queryset = Relation.objects.filter(
                    (Q(first_user=user) | Q(second_user=user)) &
                    Q(is_active=is_active)
                ).order_by("-created_at")

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
    def handle_create(data: dict):
        try:
            return Relation.objects.create(**data)
        except Exception:
            return None

    @staticmethod
    def handle_update(relation: Relation, data: dict):
        try:
            for field, value in data.items():
                setattr(relation, field, value)
            relation.save(update_fields=list(data.keys()))
            return relation
        except Exception:
            return None

    @staticmethod
    def handle_delete(relation: Relation):
        try:
            relation.is_active = False
            relation.save(update_fields=["is_active"])
            return relation
        except Exception:
            return None

    @staticmethod
    def handle_hard_delete(relation: Relation):
        try:
            relation.delete()
            return True
        except Exception:
            return None

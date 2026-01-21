import uuid
from django.core.paginator import Paginator
from django.db.models import Q

from app.entities.relation import Relation
from app.entities.profile import Profile
from app.utils.fieldsFilter import FieldsFilter


class RelationRepo:

    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = (
                    Relation.objects.select_related("first_user", "second_user")
                    .all()
                    .order_by("-created_at")
                )
            else:
                queryset = (
                    Relation.objects.select_related("first_user", "second_user")
                    .filter(is_active=is_active)
                    .order_by("-created_at")
                )

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "page": items.number,
                "page_size": page_size,
                "total_items": paginator.count,
                "data": list(items),
            }
        except Exception as e:
            raise e

    @staticmethod
    def find_by_id(relation_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return Relation.objects.select_related("first_user", "second_user").get(
                    id=relation_id
                )
            else:
                return Relation.objects.select_related("first_user", "second_user").get(
                    id=relation_id, is_active=is_active
                )
        except Relation.DoesNotExist:
            return None
        except Exception as e:
            raise e

    @staticmethod
    def handle_create(data: dict):
        try:
            return Relation.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(relation: Relation, data: dict):
        try:
            for field, value in data.items():
                setattr(relation, field, value)
            relation.save(update_fields=list(data.keys()))
            return relation
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(relation: Relation):
        try:
            relation.is_active = False
            relation.save(update_fields=["is_active"])
            return relation
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(relation: Relation):
        try:
            relation.delete()
            return True
        except Exception as e:
            raise e

    @staticmethod
    def handle_search_relations(
        search_data: dict,
        page: int = 1,
        page_size: int = 20,
    ):
        try:
            filtered_data = FieldsFilter(data=search_data, entity=Relation)
            first_user_id = filtered_data.pop("first_user_id", None) if filtered_data else None
            second_user_id = filtered_data.pop("second_user_id", None) if filtered_data else None
            user_id = filtered_data.pop("user_id", None) if filtered_data else None

            filters = Q()
            for field, value in filtered_data.items():
                filters &= Q(**{field: value})

            if first_user_id and second_user_id:
                filters &= (
                    Q(first_user__id=first_user_id, second_user__id=second_user_id)
                    | Q(first_user__id=second_user_id, second_user__id=first_user_id)
                )
            elif user_id:
                filters &= (
                    Q(first_user__id=user_id) | Q(second_user__id=user_id)
                )

            queryset = Relation.objects.select_related("first_user", "second_user").filter(filters).order_by("-created_at")

            paginator = Paginator(queryset, page_size)
            items = paginator.page(page)

            return {
                "page": items.number,
                "page_size": page_size,
                "total_items": paginator.count,
                "data": list(items),
            }
        except Exception as e:
            raise e

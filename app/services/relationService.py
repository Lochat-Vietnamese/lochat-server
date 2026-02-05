from typing import Dict

from app.entities.relation import Relation
from app.repositories.relationRepo import RelationRepo
from app.services.profileService import ProfileService
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class RelationService:
    @staticmethod
    def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")
            return RelationRepo.all(page=page, page_size=page_size, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def get_by_id(relation_id: str, is_active: bool | None = True):
        try:
            return RelationRepo.find_by_id(relation_id=relation_id, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def create(data: Dict):
        try:
            first_user_id = data.get("first_user_id")
            second_user_id = data.get("second_user_id")

            if not first_user_id or not second_user_id:
                ExceptionHelper.throw_bad_request("Missing data")
            
            if str(first_user_id) == str(second_user_id):
                ExceptionHelper.throw_bad_request("Same user")

            first_user = ProfileService.get_by_id(first_user_id)
            second_user = ProfileService.get_by_id(second_user_id)

            existing = RelationService.search_relations({"first_user_id": first_user_id, "second_user_id": second_user_id, "is_active": None})
            if existing:
                ExceptionHelper.throw_bad_request("Relation already exists")
            
            data["first_user"] = first_user
            data["second_user"] = second_user

            return RelationRepo.handle_create(FieldsFilter(data=data, entity=Relation))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def update(data: Dict):
        try:
            relation_id = data.get("id")

            relation = RelationService.get_by_id(relation_id, None)
            if not relation:
                ExceptionHelper.throw_bad_request("Relation not found")

            return RelationRepo.handle_update(relation, FieldsFilter(data=data, entity=Relation))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = RelationService.get_by_id(relation_id, None)

                return RelationRepo.handle_delete(relation)
            ExceptionHelper.throw_bad_request("Missing relation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def hard_delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = RelationService.get_by_id(relation_id, None)

                return RelationRepo.handle_hard_delete(relation)
            ExceptionHelper.throw_bad_request("Missing relation id")
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    def search_relations(search_data: Dict):
        try:
            page = search_data.pop("page")
            page_size = search_data.pop("page_size")
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request("Invalid page or page size")

            return RelationRepo.handle_search_relations(search_data=search_data, page=page, page_size=page_size)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
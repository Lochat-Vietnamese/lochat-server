import uuid
from typing import Dict
from asgiref.sync import sync_to_async

from app.repositories.relationRepo import RelationRepo
from app.services.profileService import ProfileService


class RelationService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                return None
            return await sync_to_async(RelationRepo.all)(page=page, page_size=page_size, is_active=is_active)
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_id(relation_id: str, is_active: bool | None = True):
        try:
            if relation_id and str(relation_id).strip():
                uuid_obj = uuid.UUID(relation_id)
                return await sync_to_async(RelationRepo.find_by_id)(uuid_obj, is_active)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_both_users(user1_id: str, user2_id: str, is_active: bool | None = True):
        try:
            if not user1_id or not user2_id:
                return None

            user1 = await ProfileService.get_by_id(user1_id)
            user2 = await ProfileService.get_by_id(user2_id)

            if not user1 or not user2:
                return None

            return await sync_to_async(RelationRepo.find_by_both_users)(user1, user2, is_active)
        except Exception as e:
            raise e

    @staticmethod
    async def get_by_one_user(user_id: str, page=1, page_size=20, is_active: bool | None = True):
        try:
            if not user_id:
                return None
            user = await ProfileService.get_by_id(user_id)
            if not user:
                return None

            if page <= 0 or page_size <= 0:
                return None

            return await sync_to_async(RelationRepo.find_by_one_user)(user, page, page_size, is_active)
        except Exception as e:
            raise e

    @staticmethod
    async def create(data: Dict):
        try:
            first_user_id = data.get("first_user_id")
            second_user_id = data.get("second_user_id")

            if not first_user_id or not second_user_id:
                return None
            
            if str(first_user_id) == str(second_user_id):
                return None

            first_user = await ProfileService.get_by_id(first_user_id)
            second_user = await ProfileService.get_by_id(second_user_id)

            if not first_user or not second_user:
                return None

            existing = await RelationService.get_by_both_users(first_user_id, second_user_id, None)
            if existing:
                return None
            
            data.pop("first_user_id", None)
            data.pop("second_user_id", None)
            data["first_user"] = first_user
            data["second_user"] = second_user

            return await sync_to_async(RelationRepo.handle_create)(data)
        except Exception as e:
            raise e

    @staticmethod
    async def update(data: Dict):
        try:
            relation_id = data.get("relation_id")
            if relation_id and str(relation_id).strip() and any(data.values()):
                relation = await RelationService.get_by_id(relation_id, None)
                if not relation:
                    return None
                return await sync_to_async(RelationRepo.handle_update)(relation, data)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = await RelationService.get_by_id(relation_id, None)
                if not relation:
                    return None
                return await sync_to_async(RelationRepo.handle_delete)(relation)
            return None
        except Exception as e:
            raise e

    @staticmethod
    async def hard_delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = await RelationService.get_by_id(relation_id, None)
                if not relation:
                    return None
                return await sync_to_async(RelationRepo.handle_hard_delete)(relation)
            return None
        except Exception as e:
            raise e

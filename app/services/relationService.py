import uuid
from typing import Dict
from asgiref.sync import sync_to_async

from app.dtos.profileDTOs import GetProfileByIdDTO
from app.dtos.relationDTOs import GetRelationByIdDTO, GetRelationByProfilesDTO
from app.entities.relation import Relation
from app.enums.responseMessages import ResponseMessages
from app.repositories.relationRepo import RelationRepo
from app.services.profileService import ProfileService
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter


class RelationService:
    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            return await sync_to_async(RelationRepo.all)(page=page, page_size=page_size, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_id(relation_id: str, is_active: bool | None = True):
        try:
            return await sync_to_async(RelationRepo.find_by_id)(relation_id=relation_id, is_active=is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_both_users(dto: GetRelationByProfilesDTO):
        try:

            user1 = await ProfileService.get_by_id(dto=GetProfileByIdDTO(**dto.model_dump(exclude={"second_user_id", "is_active"})))
            user2 = await ProfileService.get_by_id(dto=GetProfileByIdDTO(**dto.model_dump(exclude={"first_user_id", "is_active"})))

            return await sync_to_async(RelationRepo.find_by_both_users)(user1, user2, dto.is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_one_user(user_id: str, page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            if not user_id:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            user = await ProfileService.get_by_id(user_id)

            return await sync_to_async(RelationRepo.find_by_one_user)(user, page, page_size, is_active)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def create(data: Dict):
        try:
            first_user_id = data.get("first_user_id")
            second_user_id = data.get("second_user_id")

            if not first_user_id or not second_user_id:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            
            if str(first_user_id) == str(second_user_id):
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            first_user = await ProfileService.get_by_id(first_user_id)
            second_user = await ProfileService.get_by_id(second_user_id)

            existing = await RelationService.get_by_both_users(first_user_id, second_user_id, None)
            if existing:
                ExceptionHelper.throw_bad_request(ResponseMessages.ALREADY_EXISTS)
            
            data["first_user"] = first_user
            data["second_user"] = second_user

            return await sync_to_async(RelationRepo.handle_create)(FieldsFilter(data=data, entity=Relation))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update(data: Dict):
        try:
            relation_id = data.get("id")
            if relation_id and str(relation_id).strip() and any(data.values()):
                relation = await RelationService.get_by_id(relation_id, None)

                return await sync_to_async(RelationRepo.handle_update)(relation, FieldsFilter(data=data, entity=Relation))
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = await RelationService.get_by_id(relation_id, None)

                return await sync_to_async(RelationRepo.handle_delete)(relation)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def hard_delete(relation_id: str):
        try:
            if relation_id and str(relation_id).strip():
                relation = await RelationService.get_by_id(relation_id, None)

                return await sync_to_async(RelationRepo.handle_hard_delete)(relation)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

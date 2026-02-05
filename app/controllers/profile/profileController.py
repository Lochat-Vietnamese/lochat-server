from django.views import View

from app.dtos.profileDTOs import SearchProfilesDTO, GetProfileByIdDTO
from app.enums.responseCodes import ResponseCodes
from app.mapping.profileMapping import ProfileMapping
from app.services.profileService import ProfileService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData
from asgiref.sync import sync_to_async


class ProfileController(View):
    async def get(self, request, profile_id=None):
        try:
            raw_params = RequestData(request=request)

            if profile_id:
                get_by_id_dto = GetProfileByIdDTO(profile_id=profile_id)
                
                result = await sync_to_async(ProfileService.get_by_id)(get_by_id_dto.profile_id, is_active=True)
                return BaseResponse.success(
                    data=ProfileMapping(result).data,
                    code=ResponseCodes.GET_PROFILE_BY_ID_SUCCESS,
                    message="Get profile by id successfully",
                )
            
            search_profile_dto = SearchProfilesDTO(**raw_params)

            if search_profile_dto.is_only_pagination():
                result = await sync_to_async(ProfileService.get_all)(page=search_profile_dto.page, page_size=search_profile_dto.page_size, is_active=search_profile_dto.is_active)
                return BaseResponse.success(
                    data=ProfileMapping(result.get("data", []), many=True).data,
                    code=ResponseCodes.GET_ALL_PROFILES_SUCCESS,
                    message="Get all profile successfully",
                    page=result.get("page"),
                    page_size=result.get("page_size"),
                    total_items=result.get("total_items"),
                )
            
            result = await sync_to_async(ProfileService.search_profiles)(search_profile_dto.model_dump())
            return BaseResponse.success(
                data=ProfileMapping(result.get("data", []), many=True).data,
                code=ResponseCodes.SEARCH_PROFILE_SUCCESS,
                message="Search profile successfully",
                page=result.get("page"),
                page_size=result.get("page_size"),
                total_items=result.get("total_items"),
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
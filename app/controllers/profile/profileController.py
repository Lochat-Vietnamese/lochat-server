from django.views import View

from app.dtos.profileDTOs import SearchProfilesDTO, GetProfileByIdDTO
from app.enums.httpStatus import HttpStatus
from app.enums.responseCodes import ResponseCodes
from app.mapping.profileMapping import ProfileMapping
from app.services.profileService import ProfileService
from app.helpers.baseResponse import BaseResponse
from app.helpers.exceptionHelper import ExceptionHelper
from app.utils.requestData import RequestData

class ProfileController(View):
    async def get(self, request, profile_id=None):
        try:
            raw_params = RequestData(request=request)

            if profile_id:
                get_by_id_dto = GetProfileByIdDTO(profile_id=profile_id)
                
                result = await ProfileService.get_by_id(get_by_id_dto.profile_id, is_active=True)
                return BaseResponse.success(
                    data=ProfileMapping(result).data,
                    code=ResponseCodes.GET_PROFILE_BY_ID_SUCCESS,
                    message="Get profile by id successfully",
                )
            
            search_profile_dto = SearchProfilesDTO(**raw_params)

            if search_profile_dto:
                result = await ProfileService.search_profiles(search_profile_dto.model_dump())
                return BaseResponse.success(
                    data=ProfileMapping(result.get("content", []), many=True).data,
                    code=ResponseCodes.SEARCH_PROFILE_SUCCESS,
                    message="Search profile successfully",
                    meta={
                        "page": result.get("page"),
                        "page_size": result.get("page_size"),
                        # "total_pages": result.get("total_pages"),
                        # "total_items": result.get("total_items"),
                        # "has_next": result.get("has_next"),
                        # "has_prev": result.get("has_prev"),
                    }
                )
                
            result = await ProfileService.get_all(search_profile_dto)
            result["content"] = ProfileMapping(result.get("content", []), many=True).data
            return BaseResponse.success(
                data=result,
                code=ResponseCodes.GET_ALL_PROFILES_SUCCESS,
                message="Get all profile successfully"
            )

        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)
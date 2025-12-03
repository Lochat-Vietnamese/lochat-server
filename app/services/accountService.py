import uuid
from typing import Dict
from app.entities.account import Account
from app.enums.responseMessages import ResponseMessages
from app.repositories.accountRepo import AccountRepo
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from app.services.profileService import ProfileService
from app.utils.exceptionHelper import ExceptionHelper
from app.utils.fieldsFilter import FieldsFilter
from app.utils.redisClient import RedisClient
from asgiref.sync import sync_to_async

class AccountService:
    @staticmethod
    def is_valid_email(email: str):
        if not email or "@" not in email or "." not in email:
            return False
        return email.count("@") == 1

    @staticmethod
    async def get_all(page=1, page_size=20, is_active: bool | None = True):
        try:
            if page <= 0 or page_size <= 0:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
            return await sync_to_async(AccountRepo.all)(
                page=page, page_size=page_size, is_active=is_active
            )
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_id(account_id: str, is_active: bool | None = True):
        try:
            if account_id and str(account_id).strip():
                uuid_obj = uuid.UUID(account_id)
                return await sync_to_async(AccountRepo.find_by_id)(uuid_obj, is_active)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_username(username: str, is_active: bool | None = True):
        try:
            if username and str(username).strip():
                return await sync_to_async(AccountRepo.find_by_username)(
                    username=username, is_active=is_active
                )
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def get_by_email(email: str, is_active: bool | None = True):
        try:
            if AccountService.is_valid_email(email):
                return await sync_to_async(AccountRepo.find_by_email)(email=email, is_active=is_active)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def create(data: Dict):
        try:
            username = data.get("username")
            email = data.get("email")

            if await sync_to_async(AccountRepo.find_by_username)(username, None):
                ExceptionHelper.throw_bad_request(ResponseMessages.ALREADY_EXISTS)

            if await sync_to_async(AccountRepo.find_by_email)(email, None):
                ExceptionHelper.throw_bad_request(ResponseMessages.ALREADY_EXISTS)

            return await sync_to_async(AccountRepo.handle_create)(FieldsFilter(data=data, entity=Account))
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def update(data: Dict):
        try:
            account_id = data.get("id")
            if account_id and str(account_id).strip() and any(data.values()):
                account = await AccountService.get_by_id(account_id, None)
                if not account:
                    ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
                return await sync_to_async(AccountRepo.handle_update)(account, FieldsFilter(data=data, entity=Account))
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def delete(account_id: str):
        try:
            if account_id and str(account_id).strip():
                account = await AccountService.get_by_id(account_id, None)
                if not account:
                    ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
                return await sync_to_async(AccountRepo.handle_delete)(account)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def hard_delete(account_id: str):
        try:
            if account_id and str(account_id).strip():
                account = await AccountService.get_by_id(account_id, None)
                if not account:
                    ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
                return await sync_to_async(AccountRepo.handle_hard_delete)(account)
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def login(data: Dict):
        try:
            username = str(data.get("username")).strip()
            email = str(data.get("email")).strip()
            password = str(data.get("password")).strip()

            if not (username or email ) or not password:
                ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_INPUT)

            account = None
            if username:
                account = await AccountService.get_by_username(str(username).strip())
            elif email:
                account = await AccountService.get_by_email(str(email).strip())
            if account and check_password(password, account.password):
                refresh = RefreshToken.for_user(account)
                rd = await RedisClient.instance()
                await rd.add(
                    key=f"token_{account.id}",
                    value=str(refresh),
                    expire_sec=7 * 24 * 60 * 60,
                )
                return {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "account": account,
                }
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_CREDENTIALS)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def sign_up(data: dict):
        try:
            username = str(data.get("username")).strip()
            email = str(data.get("email")).strip()
            password = str(data.get("password")).strip()
            phone_number = str(data.get("phone_number")).strip()

            profile = await ProfileService.get_by_phone_number(
                phone_number=phone_number, is_active=None
            )
            if not profile:
                profile = await ProfileService.create(data=data)

            existingUsername = await AccountService.get_by_username(username, None)
            existingEmail = await AccountService.get_by_email(email, None)
            if not existingUsername and not existingEmail:
                data["password"] = make_password(password)
                data["profile"] = profile
                return await AccountService.create(data=data)

            ExceptionHelper.throw_bad_request(ResponseMessages.ALREADY_EXISTS)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

    @staticmethod
    async def restock_token(refresh_token: str):
        try:
            token = RefreshToken(refresh_token)
            account_id = token["user_id"]

            rd = await RedisClient.instance()
            if await rd.exists(f"token_{account_id}") != 0:
                account = await AccountService.get_by_id(account_id)
                if not account:
                    ExceptionHelper.throw_not_found(ResponseMessages.NOT_FOUND)
                
                refresh = RefreshToken.for_user(account)
                access = refresh.access_token
                await rd.add(
                    key=f"token_{account.id}",
                    value=str(refresh),
                    expire_sec=7 * 24 * 60 * 60,
                )

                return {
                    "access_token": str(access),
                    "refresh_token": str(refresh),
                    "account": account,
                }
            ExceptionHelper.throw_bad_request(ResponseMessages.INVALID_TOKEN)
        except Exception as e:
            ExceptionHelper.handle_caught_exception(error=e)

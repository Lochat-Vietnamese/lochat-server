# import uuid
# from django.utils.timezone import datetime, now
# from app.entities.accountsConversations import AccountsConversations
# from app.entities.account import Accounts
# from app.entities.conversations import Conversations
# from django.core.paginator import Paginator


# class AccountsConversationsRepo:
#     @staticmethod
#     def get_all():
#         try:
#             return AccountsConversations.objects.all()
#         except Exception:
#             return None

#     @staticmethod
#     def get_by_id(account_id: uuid.UUID):
#         try:
#             return AccountsConversations.objects.get(id=account_id)
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_account(account: Accounts):
#         try:
#             return AccountsConversations.objects.filter(account=account)
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_account_paginated(account_id: uuid.UUID, page: int, page_size: int):
#         try:
#             query = AccountsConversations.objects.filter(
#                 account__id=account_id
#             ).order_by("-last_accessed")
#             paginated = Paginator(query, page_size)
#             content = paginated.page(page)
#             return {
#                 "pages_count": paginated.num_pages,
#                 "current_page": content.number,
#                 "page_content": list(content),
#             }
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_conversation(conversation: Conversations):
#         try:
#             return AccountsConversations.objects.filter(
#                 conversation=conversation
#             ).order_by("-last_accessed")
#         except Exception:
#             return None

#     @staticmethod
#     def get_by_account_and_conversation(data: dict):
#         try:
#             account = data.get("account")
#             conversation = data.get("conversation")
#             if account and conversation:
#                 return AccountsConversations.objects.get(
#                     conversation=conversation, account=account
#                 )

#             account_id = data.get("account_id")
#             conversation_id = data.get("conversation_id")
#             if account_id and conversation_id:
#                 return AccountsConversations.objects.get(
#                     conversation__id=conversation_id, account__id=account_id
#                 )
#         except Exception:
#             return None

#     @staticmethod
#     def filter_by_date_created(date: datetime):
#         try:
#             return AccountsConversations.objects.filter(created_at=date).order_by(
#                 "-created_at"
#             )
#         except Exception:
#             return None

#     @staticmethod
#     def do_create(data: dict):
#         try:
#             return AccountsConversations.objects.create(**data)
#         except Exception:
#             return None

#     @staticmethod
#     def do_update(data: dict, accountsConversations: AccountsConversations):
#         try:
#             for field, value in data.items():
#                 setattr(accountsConversations, field, value)
#             accountsConversations.updated_at = now()
#             accountsConversations.save(update_fields=data.keys())
#             return accountsConversations
#         except Exception:
#             return None

#     @staticmethod
#     def do_delete(accountsConversations: AccountsConversations):
#         try:
#             accountsConversations.is_active = False
#             accountsConversations.updated_at = now()
#             accountsConversations.save()
#             return accountsConversations
#         except Exception:
#             return None

#     @staticmethod
#     def do_hard_delete(accountsConversations: AccountsConversations):
#         try:
#             accountsConversations.delete()
#             return True
#         except Exception:
#             return False

#     # fix here
#     @staticmethod
#     def handle_update_last_accessed(accountsConversations: AccountsConversations):
#         try:
#             accountsConversations.last_accessed = now()
#             accountsConversations.save()
#             return accountsConversations
#         except Exception:
#             return None

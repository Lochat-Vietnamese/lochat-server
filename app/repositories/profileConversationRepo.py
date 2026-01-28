import uuid
from django.utils.timezone import now
from app.entities.profileConversation import ProfileConversation
from app.entities.profile import Profile
from app.entities.conversation import Conversation
from django.core.paginator import Paginator
from django.db.models import Q

from app.enums.conversationTypes import ConversationTypes
from app.utils.fieldsFilter import FieldsFilter


class ProfileConversationRepo:
    @staticmethod
    def all(page: int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").all().order_by("-created_at")
            else:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").filter(is_active=is_active).order_by("-created_at")

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
    def find_by_id(profileConversation_id: uuid.UUID, is_active: bool | None):
        try:
            if is_active is None:
                return ProfileConversation.objects.select_related("profile", "conversation").get(id=profileConversation_id)
            return ProfileConversation.objects.select_related("profile", "conversation").get(id=profileConversation_id, is_active=is_active)
        except ProfileConversation.DoesNotExist:
            return None
        except Exception as e:
            raise e
        
    @staticmethod
    def find_by_profile(profile: Profile, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").filter(profile=profile).order_by("-last_accessed")
            else:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").filter(profile=profile, is_active=is_active).order_by("-last_accessed")

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
    def find_by_conversation(conversation: Conversation, page:int, page_size: int, is_active: bool | None):
        try:
            if is_active is None:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").filter(conversation=conversation).order_by("-last_accessed")
            else:
                queryset = ProfileConversation.objects.select_related("profile", "conversation").filter(conversation=conversation, is_active=is_active).order_by("-last_accessed")

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
    def find_by_both(profile: Profile, conversation: Conversation, is_active: bool | None):
        try:
            if is_active is None:
                return ProfileConversation.objects.select_related("profile", "conversation").get(conversation=conversation, profile=profile)
            return ProfileConversation.objects.select_related("profile", "conversation").get(conversation=conversation, profile=profile, is_active=is_active)
        except ProfileConversation.DoesNotExist:
            return None
        except Exception as e:
            raise e

    @staticmethod
    def handle_create(data: dict):
        try:
            return ProfileConversation.objects.create(**data)
        except Exception as e:
            raise e

    @staticmethod
    def handle_update(ProfileConversation: ProfileConversation, data: dict):
        try:
            for field, value in data.items():
                setattr(ProfileConversation, field, value)
            ProfileConversation.save(update_fields=list(data.keys()))
            return ProfileConversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_delete(ProfileConversation: ProfileConversation):
        try:
            ProfileConversation.is_active = False
            ProfileConversation.save(update_fields=["is_active"])
            return ProfileConversation
        except Exception as e:
            raise e

    @staticmethod
    def handle_hard_delete(ProfileConversation: ProfileConversation):
        try:
            ProfileConversation.delete()
            return True
        except Exception as e:
            raise e

    @staticmethod
    def handle_update_last_accessed(ProfileConversation: ProfileConversation):
        try:
            ProfileConversation.last_accessed = now()
            ProfileConversation.save()
            return ProfileConversation
        except Exception as e:
            raise e
        
    @staticmethod
    def find_common_conversations(prof1: Profile, prof2: Profile, is_active: bool | None, type: ConversationTypes | None):
        try:
            conv_prof1 = ProfileConversation.objects.filter(profile=prof1).values_list("conversation_id", flat=True)

            common_conversations = ProfileConversation.objects.filter(
                profile=prof2,
                conversation_id__in=conv_prof1
            ).select_related("conversation")

            if is_active is None:
                if type is None:
                    list_common = [ac.conversation for ac in common_conversations]
                else:
                    list_common = [ac.conversation for ac in common_conversations if ac.conversation.type == type]
            else:
                if type is None:
                    list_common = [ac.conversation for ac in common_conversations if ac.is_active == is_active]
                else:
                    list_common = [ac.conversation for ac in common_conversations if ac.is_active == is_active and ac.conversation.type == type]
            return list_common
        except Exception as e:
            raise e
        
    @staticmethod
    def handle_search_memberships(
        search_data: dict,
        page: int = 1,
        page_size: int = 20,
    ):
        try:
            data = FieldsFilter(data=search_data, entity=ProfileConversation)
            filters = Q()
            for field, value in data.items():
                filters &= Q(**{field: value})

            queryset = Profile.objects.filter(filters).order_by("-created_at")

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
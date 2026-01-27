"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app.controllers.account.accountController import AccountController
from app.controllers.auth.logout import Logout
from app.controllers.auth.restockToken import RestockToken
from app.controllers.auth.signUp import SignUp
from app.controllers.auth.signIn import SignIn
from app.controllers.conversation.conversationController import ConversationController
from app.controllers.media.mediaController import MediaController
from app.controllers.membership.membershipController import MembershipController
from app.controllers.message.messageController import MessageController
from app.controllers.profile.profileController import ProfileController
from app.controllers.profile.profileConversationsController import ProfileConversationsController
from app.controllers.relation.relationController import RelationController

urlpatterns = [
    path('signin', SignIn.as_view(), name='signin'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', Logout.as_view(), name='logout'),
    path('restock-token', RestockToken.as_view(), name='restock-token'),

    path('accounts/<uuid:account_id>', AccountController.as_view(), name='accounts'),
    path('conversations/<uuid:conversation_id>', ConversationController.as_view(), name='conversations'),
    path('medias/<uuid:media_id>', MediaController.as_view(), name='medias'),
    path('memberships/<uuid:membership_id>', MembershipController.as_view(), name='memberships'),
    path('messages/<uuid:message_id>', MessageController.as_view(), name='messages'),
    path('profiles/<uuid:profile_id>', ProfileController.as_view(), name='profiles'),
    path('profiles/<uuid:profile_id>/conversations', ProfileConversationsController.as_view(), name='profiles-conversations'),
    path('relations/<uuid:relation_id>', RelationController.as_view(), name='relations'),
]
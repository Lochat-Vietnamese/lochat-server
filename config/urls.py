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
from app.controllers.accountController import AccountController
from app.controllers.authController import AuthController
from app.controllers.conversationController import ConversationController
from app.controllers.profileController import ProfileController
from app.controllers.profileConversationController import ProfileConversationController
from app.controllers.relationController import RelationController; 

urlpatterns = [
    path('<str:action>', AuthController.as_view(), name='auth_action'),
    path('account/<str:action>', AccountController.as_view(), name='account_action'),
    path('profile/<str:action>', ProfileController.as_view(), name='profile_action'),
    path('relation/<str:action>', RelationController.as_view(), name='relation_action'),
    path('conversation/<str:action>', ConversationController.as_view(), name='conversation_action'),
    path('profile-conversation/<str:action>', ProfileConversationController.as_view(), name='profile_conversation_action'),
]
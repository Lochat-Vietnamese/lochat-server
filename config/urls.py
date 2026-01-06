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
from app.controllers.auth.logout import Logout
from app.controllers.auth.restockToken import RestockToken
from app.controllers.auth.signUp import SignUp
from app.controllers.auth.signIn import SignIn

urlpatterns = [
    path('signin', SignIn.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', Logout.as_view(), name='logout'),
    path('restock-token', RestockToken.as_view(), name='restock-token'),

    
]
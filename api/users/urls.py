from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import CreateUser, GetUser, Login

urlpatterns = [
    path('', CreateUser.as_view(), name="create_user"),
    path('/me', GetUser.as_view(), name="get_user"),
    path('/auth', Login.as_view(), name='login'),
    path('/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
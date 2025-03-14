from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import CreateUser, GetUser, UpdateUser, Login

urlpatterns = [
    path('signup', CreateUser.as_view(), name="create_user"),
    path('me', GetUser.as_view(), name="get_current_user"),
    path('update', UpdateUser.as_view(), name="update_user"),
    path('login', Login.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
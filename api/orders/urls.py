from django.urls import path
from .views import OrderList, OrderDetail, CreateOrder

urlpatterns = [
    path("", OrderList.as_view(), name="list-my-order"),
    path("<int:pk>", OrderDetail.as_view(), name="order-details"),
    path("create", CreateOrder.as_view(), name="create-order"),
]

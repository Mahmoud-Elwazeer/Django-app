from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer

class OrderList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Return orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the authenticated user
        serializer.save(user=self.request.user)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Return orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

class CreateOrder(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def perform_create(self, serializer):
        # Set the user to the authenticated user
        serializer.save(user=self.request.user)

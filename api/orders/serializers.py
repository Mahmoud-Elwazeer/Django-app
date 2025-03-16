from rest_framework import serializers
from .models import Order, OrderItem
from api.products.serializers import ProductSerializer  # Assuming you have a ProductSerializer
from api.products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name") 

    class Meta:
        model = OrderItem
        fields = ["product_name", "quantity", "price", "total_price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Include order items
    # user = serializers.StringRelatedField(read_only=True)  # Include user details

    class Meta:
        model = Order
        fields = [
            "status", "total_price", "shipping_price", "total_quantity",
            "created_at", "updated_at", "items"
        ]
        read_only_fields = ["total_price", "total_quantity", "created_at", "updated_at"]

class CreateOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

class CreateOrderSerializer(serializers.Serializer):
    order = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    orderItems = CreateOrderItemSerializer(many=True)

    def validate(self, data):
        # Validate order data
        order_data = data["order"]
        if "totalPrice" not in order_data:
            raise serializers.ValidationError({"order": "totalPrice is required."})
        if "shippingPrice" not in order_data:
            raise serializers.ValidationError({"order": "shippingPrice is required."})

        # Validate order items
        order_items = data["orderItems"]
        if not order_items:
            raise serializers.ValidationError({"orderItems": "At least one order item is required."})

        # Validate total price
        total_price = 0
        for item in order_items:
            product = item["product"]
            quantity = item["quantity"]
            total_price += product.price * quantity

        # Add shipping price
        shipping_price = order_data["shippingPrice"]
        total_price += shipping_price

        # Compare with the total price provided by the client
        if total_price != order_data["totalPrice"]:
            raise serializers.ValidationError({"totalPrice": "Total price does not match the calculated price."})

        return data

    def create(self, validated_data):
        # Extract order and order items data
        order_data = validated_data["order"]
        order_items_data = validated_data["orderItems"]

        # Create the order
        order = Order.objects.create(
            user=self.context["request"].user,
            total_price=order_data["totalPrice"],
            shipping_price=order_data["shippingPrice"],
            status="pending",  # Default status
        )

        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data["product"],
                quantity=item_data["quantity"],
                price=item_data["product"].price,  # Use the product's price
            )

        # Calculate totals (optional, if you want to ensure consistency)
        order.calculate_totals()

        return order

    def to_representation(self, instance):
        # Serialize the created Order instance
        return {
            "id": instance.id,
            "user": instance.user.email,
            "status": instance.status,
            "total_price": instance.total_price,
            "shipping_price": instance.shipping_price,
            "total_quantity": instance.total_quantity,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }

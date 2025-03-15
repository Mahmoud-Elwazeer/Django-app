from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "parent", "subcategories"]

    def get_subcategories(self, obj):
        # Fetch only direct subcategories of this category
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "category", "category_id",
            "is_stored", "available_quantity", "main_image", "optional_image1",
            "optional_image2", "optional_image3"
        ]

    def validate(self, data):
        """Ensure stored products require quantity, and non-stored ones don’t."""
        if data.get("is_stored") and ("available_quantity" not in data or data["available_quantity"] is None):
            raise serializers.ValidationError({"available_quantity": "Stored products must have available quantity."})
        if not data.get("is_stored"):
            data["available_quantity"] = None  # Ignore quantity for non-stored products
        return data

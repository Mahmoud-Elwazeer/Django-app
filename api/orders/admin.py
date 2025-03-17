from django.contrib import admin
from .models import Order, OrderItem
from api.users.models import Profile

class OrderItemInline(admin.TabularInline):  # Inline for order items
    model = OrderItem
    extra = 0  # No extra empty fields to add new items
    can_delete = False  # Disable deletion of OrderItem instances
    max_num = 0  # Prevent adding new OrderItem instances

    def has_add_permission(self, request, obj=None):
        """
        Disable the ability to add new OrderItem instances.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Disable the ability to change existing OrderItem instances.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disable the ability to delete existing OrderItem instances.
        """
        return False

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only.
        """
        return [f.name for f in self.model._meta.fields]

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "shipping_price", "total_quantity", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "status")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]  # Add OrderItemInline

    # Customize the form to display user and profile details
    fieldsets = (
        ("Order Information", {
            "fields": ("user", "status", "total_price", "shipping_price", "total_quantity", "created_at", "updated_at"),
        }),
        ("User Details", {
            "fields": ("user_username", "user_email", "user_first_name", "user_last_name"),
        }),
        ("Profile Details", {
            "fields": ("user_phone", "user_addressLine1", "user_addressLine2", "user_city", "user_state", "user_postalCode", "user_country"),
        }),
    )
    

    # Add read-only fields for user and profile details
    readonly_fields = (
        "user", "total_price", "shipping_price", "total_quantity", 
        "user_username", "user_email", "user_first_name", "user_last_name",
        "user_phone", "user_addressLine1", "user_addressLine2", "user_city", "user_state", "user_postalCode", "user_country",
        "created_at", "updated_at"
    )

    # Custom methods for user details
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = "Username"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = "First Name"

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = "Last Name"

    # Custom methods for profile details
    def user_phone(self, obj):
        return obj.user.profile.phone
    user_phone.short_description = "Phone"

    def user_addressLine1(self, obj):
        return obj.user.profile.addressLine1
    user_addressLine1.short_description = "Address Line 1"

    def user_addressLine2(self, obj):
        return obj.user.profile.addressLine2
    user_addressLine2.short_description = "Address Line 2"

    def user_city(self, obj):
        return obj.user.profile.city
    user_city.short_description = "City"

    def user_state(self, obj):
        return obj.user.profile.state
    user_state.short_description = "State"

    def user_postalCode(self, obj):
        return obj.user.profile.postalCode
    user_postalCode.short_description = "Postal Code"

    def user_country(self, obj):
        return obj.user.profile.country
    user_country.short_description = "Country"

    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to handle order cancellation.
        """
        if change:  # Check if the order is being updated (not created)
            old_order = Order.objects.get(pk=obj.pk)  # Get the old order instance
            if old_order.status != "cancelled" and obj.status == "cancelled":
                # If the order is being cancelled, update the product quantities
                self.update_product_quantities(obj)

        super().save_model(request, obj, form, change)

    def update_product_quantities(self, order):
        """
        Update the available_quantity of products when an order is cancelled.
        """
        for item in order.items.all():
            product = item.product
            if product.is_stored:
                product.available_quantity += item.quantity  # Increase the available quantity
                product.save()

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price", "total_price")
    search_fields = ("order__user__username", "product__name")

    readonly_fields = ("order", "product", "quantity", "price")

    def total_price(self, obj):
        return obj.total_price()  # Call total_price method from model
    total_price.short_description = "Total Price"

# Register models
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
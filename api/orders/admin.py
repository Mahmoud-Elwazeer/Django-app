from django.contrib import admin
from .models import Order, OrderItem
from api.users.models import Profile

class OrderItemInline(admin.TabularInline):  # Inline for order items
    model = OrderItem
    extra = 1  # Show empty fields to add new items

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

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price", "total_price")
    search_fields = ("order__user__username", "product__name")

    def total_price(self, obj):
        return obj.total_price()  # Call total_price method from model
    total_price.short_description = "Total Price"

# Register models
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
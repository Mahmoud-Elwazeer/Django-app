from django.urls import path, include

from .views import CategoryList, ProductList, ProductDetails

urlpatterns = [
    path('categories', CategoryList.as_view(), name="list_categories"),
    path('', ProductList.as_view(), name="list_products"),
    path('<int:id>', ProductDetails.as_view(), name='product_details'),
]
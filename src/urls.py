"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# for normal user using JWT
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Restrict access to admin users only
def admin_required(user):
    return user.is_authenticated and user.is_staff  # Only allow staff (admin) users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include("api.users.urls")),
    path('api/v1/products/', include("api.products.urls")),
    path('api/v1/orders/', include("api.orders.urls")),


    # Spectacular API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # # Protect Swagger UI with authentication
    # path('api/docs/', login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    # # Protect ReDoc UI with authentication
    # path('api/redoc/', login_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),

    path('api/docs/', user_passes_test(admin_required)(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path('api/redoc/', user_passes_test(admin_required)(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

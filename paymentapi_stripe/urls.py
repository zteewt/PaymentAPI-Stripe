from django.contrib import admin
from django.urls import path, include
from product.views import CreateCheckoutSessionView, ItemPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
]
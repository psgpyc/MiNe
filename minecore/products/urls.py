from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)

app_name = 'products'

urlpatterns = [
    path('', include(router.urls))
]

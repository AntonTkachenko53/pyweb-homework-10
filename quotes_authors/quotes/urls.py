from rest_framework import routers
from .views import QuoteViewSet, TagViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'', QuoteViewSet)
router.register(r'', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tags/', TagViewSet.as_view({'get': 'list'})),
]

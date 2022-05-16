from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import SubscriptionsViewSet, subscribe

v1_router = SimpleRouter()
v1_router.register(
    'subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions'
)
urlpatterns = [
    path('users/', include(v1_router.urls)),
    path('users/<int:id>/subscribe/', subscribe, name='subscribe'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
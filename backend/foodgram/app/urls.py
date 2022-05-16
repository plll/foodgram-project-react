from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (IngredientsViewSet, RecipeViewSet, TagsViewSet, favorite,
                    shopping_cart)

v1_router = SimpleRouter()
v1_router.register(
    'tags',
    TagsViewSet,
    basename='tags'
)
v1_router.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
v1_router.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)
urlpatterns = [
    path('', include(v1_router.urls)),
    path('recipes/<int:id>/favorite/', favorite, name='favorite'),
    path('recipes/<int:id>/shopping_cart/', shopping_cart ,name='shopping_cart'),
]

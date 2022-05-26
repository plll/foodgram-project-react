from django.contrib import admin

from users.models import Subscription, User
from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)
from .forms import TagForm


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_editable = ('color',)


@admin.register(Recipe)
class RecipiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recipe_description', 'text', 'image', 'cooking_time')
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'follower')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')


@admin.register(IngredientInRecipe)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe')

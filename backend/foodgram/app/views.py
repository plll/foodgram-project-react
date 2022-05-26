from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .filters import IngredientFilter, UserRecipeFilter
from .models import Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingCart, Tag
from .permissions import AuthorOrReadOnly
from .serializers import (AboutRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerizlizer)


class RetriveListGenericViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    search_fields = ('id',)
    pagination_class = None


class TagsViewSet(RetriveListGenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerizlizer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrReadOnly,]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_class = UserRecipeFilter
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        if serializer['ingredients'] != []:
            serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        cart = ShoppingCart.objects.filter(user=request.user)
        recipes = (one.recipe for one in cart)
        shopping_list = {}
        shopping_list_measurement = {}
        for recipe in recipes:
            ingredients = IngredientInRecipe.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                try:
                    if shopping_list[ingredient.ingredient.name] != 0:
                        pass
                except Exception:
                    shopping_list[ingredient.ingredient.name] = ingredient.amount
                    shopping_list_measurement[ingredient.ingredient.name] = ingredient.ingredient.measurement_unit
                else:
                    shopping_list[ingredient.ingredient.name] += ingredient.amount
        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('timesnewroman', 'timesnewroman.ttf', 'UTF-8')) 
        p.setFont("timesnewroman", 35)
        p.drawString(200, 800, 'Список покупок')
        p.setFont("timesnewroman", 20)
        x = 750
        for key, value in shopping_list.items():
            str = f'{key} :  {value} {shopping_list_measurement[key]}'
            p.drawString(100,x, str)
            x -= 25
        p.showPage() 
        p.save()
        ShoppingCart.objects.filter(user=request.user).delete()
        return response


class IngredientsViewSet(RetriveListGenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_class = IngredientFilter


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        try:
            if_already_exists = Favorite.objects.filter(recipe=recipe).get(user=request.user)
        except Exception:
            favorite = Favorite(recipe=recipe, user=request.user)
            favorite.save()
            serializer = AboutRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'errors': 'Рецепт уже добавлен в избранное'},
                status=status.HTTP_400_BAD_REQUEST
            )
    if request.method == "DELETE":
        try:
            if_exists = Favorite.objects.filter(recipe=recipe).get(user=request.user)
        except Exception:
            return Response(
                {'errors': 'Рецепта не было в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            Favorite.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def shopping_cart(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        if_already_exists = ShoppingCart.objects.filter(recipe=recipe, user=request.user).exists()
        if if_already_exists:
            return Response(
                {'erorrs': 'Рецепт уже добавлен в корзину'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.create(recipe=recipe, user=request.user)
        serializer = AboutRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        if_already_exists = ShoppingCart.objects.filter(recipe=recipe, user=request.user).exists()
        if not if_already_exists:
            return Response(
                {'erorrs': 'Рецепт уже удален из корзины'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ShoppingCart.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

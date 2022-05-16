import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

from users.models import User
from .validators import check_slug, color_check


class Tag(models.Model):
    name = models.CharField('Название категории', max_length=200, unique=True)
    color = models.CharField('Цвет HEX', max_length=7, validators=[color_check])
    slug = models.CharField('Slug', max_length=200, unique=True, validators=[check_slug])

    def clean(self):
        str = '^[-a-zA-Z0-9_]+$'
        if re.match(str, self.slug) is None:
            raise ValidationError(
                'Слаг должен содержать цифры и латинские буквы'   
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Ingredient(models.Model):
    name = models.CharField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('В чем измеряется', max_length=50)

    def __str__(self):
        return str(self.name)


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipies'
    )
    name = models.CharField('Название', max_length=200)
    recipe_description = models.TextField('Описание')
    text = models.TextField('Текст поста')
    image = models.ImageField(upload_to='media/recipes/', 
                              verbose_name='Картинка рецепта')
    cooking_time = models.IntegerField('Время приготовления', validators=(
            validators.MinValueValidator(
                1, message='Минимальное время приготовления 1 минута'),))
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.name)


class IngredientInRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipies_using_ingredient'
    )
    amount = models.IntegerField('Кол-во продукта')


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipies'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorite_recipe'
    )


class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_recipies'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppin_recipe'
    )
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.expressions import F
from django.db.models.query_utils import Q


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='Вы уже подписывались на данного автора!'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='Подсписываться на себя нельзя!'
            )
        ]
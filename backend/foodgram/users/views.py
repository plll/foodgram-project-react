from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer

User = get_user_model()


class ListGenericViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    pass


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, id):
    try:
        user = User.objects.get(id=id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        if_already_exists = Subscription.objects.filter(author=user, follower=request.user).exists()
        if if_already_exists or request.user == user:
            return Response({
                'errors': 'Вы уже подписаны или пытаетесь подписаться на самого себя'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        new_sub = Subscription.objects.create(author=user, follower=request.user)
        serializer = SubscriptionSerializer(
            new_sub, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    if request.method == "DELETE":
        if_already_exists = Subscription.objects.filter(author=user, follower=request.user).exists()
        if not if_already_exists:  
            return Response(
                {'errors': 'Вы не были подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.filter(author=user, follower=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(ListGenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        limit = self.kwargs.get('recipes_limit')
        if limit is not None:
            return Subscription.objects.filter(follower=self.request.user)[:limit]
        return Subscription.objects.filter(follower=self.request.user)

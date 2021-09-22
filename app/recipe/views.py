from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class BaseRecipeAttributeViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin):
    '''Base viewset for user owned recipe attributes'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''Returns objects only for current auth user'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''create new object'''
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttributeViewSet):
    '''Manage tags in db'''
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttributeViewSet):
    '''Manage ingredients in the db'''
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

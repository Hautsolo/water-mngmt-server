from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from watermgmtapi.models import Category


class CategoryView(ViewSet):
    """Water-mgmt categorys view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all categorys

        Returns:
            Response -- JSON serialized list of categorys
        """
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True, context={'request': request})
        return Response(serializer.data)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys"""
    class Meta:
        model = Category
        fields = ('id', 'label')

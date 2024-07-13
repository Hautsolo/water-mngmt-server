from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from watermgmtapi.models import Category


class CategoryView(ViewSet):
    """Level up categorys view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
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
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """
        category = Category.objects.create(
            label=request.data["label"],
        )
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game type

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.label = request.data["label"]
            category.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a game type

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys"""
    class Meta:
        model = Category
        fields = ('id', 'label')

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from watermgmtapi.models import Post, Like
from django.db.models import Count

class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'label')
        
class LikesView(ViewSet):
  
    def retrieve(self, request, pk):
        try:
            like = Like.objects.get(pk=pk)
            serializer = LikesSerializer(like)
            return Response(serializer.data)
        except like.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        likes = Like.objects.all()
        serializer = LikesSerializer(likes)
        return Response(serializer.data)
      
    def create(self, request):

        like = Like.objects.create(
            label = request.data['label'],
        )

        serializer = LikesSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def destroy(self, request, pk):
        like = Like.objects.get(pk=pk)
        like.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

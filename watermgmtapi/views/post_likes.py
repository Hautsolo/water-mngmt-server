from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from watermgmtapi.models import User, Like, PostLike, Post
from rest_framework.decorators import action



class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'user_id', 'post_id', 'like_id')
class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'label')

class PostLikeView(ViewSet):
      def retrieve(self, request, pk):
          try:
              post_like = PostLike.objects.get(pk=pk)
              serializer = PostLikeSerializer(post_like)
              return Response(serializer.data)
          except post_like.DoesNotExist as ex:
              return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
      def list(self, request):
          post_likes = PostLike.objects.all()
          serializer = PostLikeSerializer(post_likes, many=True)
          return Response(serializer.data)
      
      def create(self, request):
          user = User.objects.get(uid=request.data['user_id'])
          post = Post.objects.get(pk=request.data['post_id'])
          like = Like.objects.get(pk=request.data['like_id'])
          
          post_like = PostLike.objects.create(
            user = user,
            post = post,
            like = like
          )

          serializer = PostLikeSerializer(post_like)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        
      # def update(self, request, pk):
      #     post_like = PostLike.objects.get(pk=pk)
      #     user = User.objects.get(pk=request.data['user_id'])
      #     post_like.user = user
          
      #     post = Post.objects.get(pk=request.data['post_id'])
      #     post_like.post = post
          
      #     like = PostLike.objects.get(pk=request.data['like_id'])
      #     post_like.like = like
      #     post_like.save()
          
      #     serializer = PostLikeSerializer(post_like)
      #     return Response(serializer.data, status=status.HTTP_200_OK)
        
      def destroy(self, request, pk):
          post_like = PostLike.objects.get(pk=pk)
          post_like.delete()
          return Response(None, status=status.HTTP_204_NO_CONTENT)

      @action(methods=['get'], detail=True)
      def get_likes_of_post(self, request, pk):
          post_likes = PostLike.objects.filter(post_id=pk)
          likes_on_post = []

          for post_like in post_likes:
              like_obj = Like.objects.get(pk=post_like.like_id)
              found = False
              for like in likes_on_post:
                  if post_like.like_id == like.get('id'):
                      like['amount'] += 1
                      like['like'] = like_obj
                      found = True
                      break
                  if not found:
                      likes_on_post.append({
                        'id': post_like.like.id,
                        'amount': 1,
                        'reaction': like_obj
                      })
          for like in likes_on_post:
              like['like'] = LikesSerializer(like['like'], many=False).data
          return Response(likes_on_post)

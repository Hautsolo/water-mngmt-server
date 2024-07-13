from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from watermgmtapi.models import User, Post, Category, Comment
from rest_framework.decorators import action
from django.db.models import Count

class PostSerializer(serializers.ModelSerializer):
  comment_count = serializers.IntegerField(default=None)
  class Meta:
    model=Post
    fields = ('id', 'title', 'category', 'description', 'image_url', 'user_id', 'comment_count')
    depth = 1
    
class PostView(ViewSet):
    def retrieve(self, request, pk):
        post = Post.objects.annotate(comment_count=Count('comments')).get(pk = pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def list(self,request):
        posts = Post.objects.annotate(comment_count=Count('comments')).all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        user_id = User.objects.get(pk = request.data["userId"])
        category = Category.objects.get(pk = request.data["categoryid"])
        
        post = Post.objects.create(
            user_id = user_id,
            category =  category,
            title = request.data["title"],
            image_url = request.data["image_url"],
            description = request.data["description"]
        )
        
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def update(self,request, pk):
        post = Post.objects.get(pk = pk)
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.description = request.data["description"]
        
        user_id=User.objects.get(pk=request.data["userId"])
        post.user_id=user_id
        
        post.save()
    
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
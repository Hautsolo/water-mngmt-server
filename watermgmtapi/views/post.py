from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from watermgmtapi.models import User, Post, Category, Comment, PostTag, Like
from rest_framework.decorators import action
from django.db.models import Count


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(default=None)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'description',
                  'image_url', 'user', 'comment_count', 'like', 'tag')
        depth = 1


class PostView(ViewSet):
    def retrieve(self, request, pk):
        post = Post.objects.annotate(
            comment_count=Count('comments')).get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def list(self, request):
        posts = Post.objects.annotate(comment_count=Count('comments')).all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = User.objects.get(pk=request.data["user_id"])
        category = Category.objects.get(pk=request.data["category_id"])
        like = Like.objects.get(pk=request.data["like_id"])
        tag = PostTag.objects.get(pk=request.data["tag_id"])

        post = Post.objects.create(
            user=user,
            category=category,
            tag=tag,
            like=like,
            title=request.data["title"],
            image=request.data["image_url"],
            description=request.data["description"]
        )

        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.image = request.data["image_url"]
        post.description = request.data["description"]

        user = User.objects.get(pk=request.data["user_id"])
        post.user = user

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

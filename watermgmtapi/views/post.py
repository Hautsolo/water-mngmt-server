from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from watermgmtapi.models import User, Post, Category, Comment, PostTag, Tag
from rest_framework.decorators import action
from django.db.models import Count


class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(default=None)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'description', 'image_url',
                  'user', 'comment_count', 'tags', 'user_id')
        depth = 2


class PostView(ViewSet):
    def retrieve(self, request, pk):
        try:
            post = Post.objects.annotate(comment_count=Count('comments')).get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        try:
            user = request.query_params.get('uid', None)
            if user is not None:
                user_id = User.objects.get(uid=user)
                posts = Post.objects.filter(user=user_id).annotate(comment_count=Count('comments'))
            else:
                posts = Post.objects.annotate(comment_count=Count('comments')).all()

            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occured: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        user = User.objects.get(uid=request.data["uid"])
        category = Category.objects.get(pk=request.data["category"])

        post = Post.objects.create(
            user=user,
            category=category,
            title=request.data["title"],
            image_url=request.data["image_url"],
            description=request.data["description"]
        )
        for tag_id in request.data["tags"]:
            tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(
                post=post,
                tag=tag
            )
        new_tags = []
        for tag in request.data["newTags"]:
            new_tag = Tag.objects.create(
                label=tag
            )
            new_tags.append(new_tag)
        for tag in new_tags:
            new_tag_2 = Tag.objects.get(pk=tag.id)
            PostTag.objects.create(
                post=post,
                tag=new_tag_2
            )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.description = request.data["description"]
        post.category = category

        post_tags = PostTag.objects.filter(post_id=post.id)
        for tag in post_tags:
            tag.delete()

        post.save()

        for tag_id in request.data["tags"]:
            tag = Tag.objects.get(pk=tag_id)
            PostTag.objects.create(
                post=post,
                tag=tag
            )
            
        new_tags = []
        for tag in request.data["newTags"]:
            new_tag = Tag.objects.create(
                label=tag
            )
            new_tags.append(new_tag)
        for tag in new_tags:
            new_tag_2 = Tag.objects.get(pk=tag.id)
            PostTag.objects.create(
                post=post,
                tag=new_tag_2
            )

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # This action method gets all comments associated with a single post
    @action(methods=['get'], detail=True, url_path='comments')
    def comments(self, request, pk=None):
        try:
            post = self.get_object()
            comments = Comment.objects.filter(post_id=pk)
            serializer = Comment.objects.filter(comments, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # This action method posts comments on a single post
    @action(methods=['post'], detail=True)
    def post_comments(self, request, pk):
        try:
            # retrieve user and post based on request data
            user = User.objects.get(pk=request.data["user"])
            post = Post.objects.get(pk=pk)
            comment = Comment.objects.create(
                user=user,
                post=post,
                content=request.data["content"]
            )
            return Response({'message': 'Comment has been successfully added'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

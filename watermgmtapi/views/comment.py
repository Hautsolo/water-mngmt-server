from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from watermgmtapi.models import Comment, User, Post


class CommentView(ViewSet):
    """Water-mgmt comments view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        post_id = request.query_params.get('post_id', None)
        if post_id is not None:
            comments = Comment.objects.filter(post_id=post_id)
        else:
            comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized comment instance
        """
        user = User.objects.get(pk=request.data["userId"])
        post = Post.objects.get(pk=request.data['post_id'])

        comment = Comment.objects.create(
            content = request.data["content"],
            user = user,
            post = post,
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a comment

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            # user = User.objects.get(pk=request.data["userId"])
            comment = Comment.objects.get(pk=pk)
            comment.content = request.data["content"]
            comment.save()
            # comment.user = user
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Handle DELETE requests for a comment

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'post', 'created_on')
        read_only_fields = ['created_on']

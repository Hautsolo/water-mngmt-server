from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from watermgmtapi.models import User


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fiels = ("id", "first_name", "last_name", "bio", "uid")


class UserView(ViewSet):
    """User Views"""

    def retrieve(self, request, pk):
        """func to get single user"""
        try:
            user = User.objects.get(uid=pk)
        except User.DoesNotExist:
            return Response("")

    def list(self, request):
        """func to list all users"""
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """func to create user"""
        user = User.objects.create(
            first_name=request.data["firstName"],
            last_name=request.data["lastName"],
            bio=request.data["bio"],
            uid=request.data["uid"]
        )

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """func to update user"""
        user = User.objects.get(pk=pk)
        user.first_name = request.data["firstName"]
        user.last_name = request.data["lastName"]
        user.bio = request.data["bio"]
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """func to del user"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

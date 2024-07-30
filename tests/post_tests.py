from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watermgmtapi.models import Post, User
from watermgmtapi.views.post import PostSerializer

class PostTests(APITestCase):
    fixtures = ['categorys', 'posts', 'users']
    
    def setUp(self):
        self.user = User.objects.first()
        
    def test_create_post(self):
        """create posot test"""
        url = "/posts"
        
        user = User.objects.first()
        
        post = {
          "title": "water bottlez",
          "image_url": "url",
          "category": 1,
          "description": "desc",
          "uid": user.uid
        }
        
        response = self.client.post(url, post, format='json')
        new_post = Post.objects.last()
        expected = PostSerializer(new_post)
        self.assertEqual(expected.data, response.data)
        
    def test_get_post(self):
        post = Post.objects.last()
        
        url = f'/posts/{post.id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected = PostSerializer(post)
        self.assertEqual(expected.data, response.data)

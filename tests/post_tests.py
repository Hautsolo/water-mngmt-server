from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from watermgmtapi.models import Post, User, Tag
from watermgmtapi.views.post import PostSerializer

class PostTests(APITestCase):
    fixtures = ['categorys', 'posts', 'users']
    
    def setUp(self):
        self.user = User.objects.first()
        
        self.tag1 = Tag.objects.create(label="Tag1")
        self.tag2 = Tag.objects.create(label="Tag2")
        
    def test_create_post(self):
        """create posot test"""
        url = "/posts"
        
        user = User.objects.first()
        
        post = {
          "title": "water bottlez",
          "image_url": "url",
          "category": 1,
          "description": "desc",
          'tags': [self.tag1.id, self.tag2.id],
          'newTags': [],
          "uid": user.uid
        }
        
        response = self.client.post(url, post, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        new_post = Post.objects.last()
        expected = PostSerializer(new_post)
        self.assertEqual(expected.data, response.data)
        
        return new_post.id
        
    def test_get_post(self):
        post_id = self.test_create_post()
        self.assertIsNotNone(post_id)
        
        url = f'/posts/{post_id}'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        expected = serializer.data
        
        for field in ['id', 'title', 'image_url', 'category', 'description', 'user_id']:
            self.assertEqual(expected[field], response.data[field])

        self.assertEqual(expected['category']['id'], response.data['category']['id'])
        self.assertEqual(expected['category']['label'], response.data['category']['label'])

        self.assertEqual(expected['user']['id'], response.data['user']['id'])
        self.assertEqual(expected['user']['name'], response.data['user']['name'])
        self.assertEqual(expected['user']['uid'], response.data['user']['uid'])
        self.assertEqual(expected['user']['bio'], response.data['user']['bio'])

        # Compare tags
        expected_tags = set((tag['id'], tag['label']) for tag in expected['tags'])
        response_tags = set((tag['id'], tag['label']) for tag in response.data['tags'])
        self.assertEqual(expected_tags, response_tags)
        
    def test_list_posts(self):
        self.test_create_post()
        self.test_create_post()
        self.test_create_post()
      
        url = '/posts'
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        
        self.assertEqual(len(response.data), Post.objects.count())
 
    def test_update_post(self):

        post_id = self.test_create_post()
        self.assertIsNotNone(post_id)
        
        url = f'/posts/{post_id}'
        
        updated_data = {
            "title": "Updated water bottle",
            "image_url": "new_url",
            "category": 2, 
            "description": "Updated description",
            'tags': [self.tag2.id],
            'newTags': [],
            "uid": self.user.uid
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        updated_post = Post.objects.get(id=post_id)
        
        self.assertEqual(updated_post.title, updated_data['title'])
        self.assertEqual(updated_post.image_url, updated_data['image_url'])
        self.assertEqual(updated_post.category.id, updated_data['category'])
        self.assertEqual(updated_post.description, updated_data['description'])
        
        # Check tags
        self.assertEqual(updated_post.tags.count(), 1)
        self.assertIn(self.tag2, updated_post.tags.all())

        serializer = PostSerializer(updated_post)
        self.assertEqual(serializer.data, response.data)
        
        return updated_post.id

    def test_destroy_post(self):
        post_id = self.test_update_post()
        self.assertIsNotNone(post_id)
        
        self.assertTrue(Post.objects.filter(id=post_id).exists())
        
        url = f'/posts/{post_id}'
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(Post.objects.filter(id=post_id).exists())
        
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)

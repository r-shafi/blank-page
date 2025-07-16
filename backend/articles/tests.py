from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Article
from categories.models import Category
from tags.models import Tag

User = get_user_model()


class ArticleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.article = Article.objects.create(
            title='Test Article',
            content='Test content',
            excerpt='Test excerpt',
            author=self.user,
            featured_image='http://example.com/image.jpg',
            status='published'
        )
        self.article.categories.add(self.category)
        self.article.tags.add(self.tag)

    def test_create_article(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Article',
            'content': 'New content',
            'excerpt': 'New excerpt',
            'featured_image': 'http://example.com/new.jpg',
            'category_ids': [self.category.id],
            'tag_ids': [self.tag.id]
        }
        response = self.client.post(reverse('article_list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 2)

    def test_search_articles(self):
        Article.objects.create(
            title='Search Test',
            content='Unique content',
            excerpt='Test excerpt',
            author=self.user,
            featured_image='http://example.com/image2.jpg',
            status='published'
        )
        response = self.client.get(
            reverse('article_list'), {'search': 'unique'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_article(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(
            reverse('article_detail', kwargs={'pk': self.article.id}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.get(
            id=self.article.id).title, 'Updated Title')

    def test_delete_article(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('article_detail', kwargs={'pk': self.article.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

    def test_unauthorized_article_operations(self):
        data = {
            'title': 'Unauthorized Article',
            'content': 'Content',
            'excerpt': 'Excerpt',
            'featured_image': 'http://example.com/unauth.jpg'
        }
        response = self.client.post(reverse('article_list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_slug_generation(self):
        article = Article.objects.create(
            title='Test Slug Generation',
            content='Content',
            excerpt='Excerpt',
            author=self.user,
            featured_image='http://example.com/image3.jpg'
        )
        self.assertEqual(article.slug, 'test-slug-generation')

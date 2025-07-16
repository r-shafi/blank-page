#!/usr/bin/env python
"""
Script to test the engagement features (likes, dislikes, bookmarks) and view counts.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from articles.models import Article, ArticleLike, BookmarkedArticle
from categories.models import Category
from tags.models import Tag

User = get_user_model()

def create_test_data():
    """Create test data for engagement features."""
    print("Creating test data...")
    
    # Create test users
    admin_user, created = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'name': 'Admin User',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.email}")
    
    author_user, created = User.objects.get_or_create(
        email='author@example.com',
        defaults={
            'name': 'Author User',
            'role': 'author',
        }
    )
    if created:
        author_user.set_password('author123')
        author_user.save()
        print(f"Created author user: {author_user.email}")
    
    reader_user, created = User.objects.get_or_create(
        email='reader@example.com',
        defaults={
            'name': 'Reader User',
            'role': 'reader',
        }
    )
    if created:
        reader_user.set_password('reader123')
        reader_user.save()
        print(f"Created reader user: {reader_user.email}")
    
    # Create test category and tag
    category, created = Category.objects.get_or_create(
        name='Technology',
        defaults={'description': 'Technology related articles'}
    )
    if created:
        print(f"Created category: {category.name}")
    
    tag, created = Tag.objects.get_or_create(
        name='Django',
        defaults={'description': 'Django framework'}
    )
    if created:
        print(f"Created tag: {tag.name}")
    
    # Create test articles
    article1, created = Article.objects.get_or_create(
        title='Test Article 1',
        defaults={
            'slug': 'test-article-1',
            'excerpt': 'This is a test article for engagement features.',
            'content': '<p>This is the content of test article 1. It should have some likes and views.</p>',
            'author': author_user,
            'status': 'published',
            'views': 25,
        }
    )
    if created:
        article1.categories.add(category)
        article1.tags.add(tag)
        print(f"Created article: {article1.title}")
    
    article2, created = Article.objects.get_or_create(
        title='Test Article 2',
        defaults={
            'slug': 'test-article-2',
            'excerpt': 'Another test article for engagement features.',
            'content': '<p>This is the content of test article 2. It should have some dislikes and bookmarks.</p>',
            'author': author_user,
            'status': 'published',
            'views': 10,
        }
    )
    if created:
        article2.categories.add(category)
        article2.tags.add(tag)
        print(f"Created article: {article2.title}")
    
    # Create engagement data
    like1, created = ArticleLike.objects.get_or_create(
        user=reader_user,
        article=article1,
        defaults={'is_like': True}
    )
    if created:
        print(f"Reader liked article 1")
    
    like2, created = ArticleLike.objects.get_or_create(
        user=admin_user,
        article=article1,
        defaults={'is_like': True}
    )
    if created:
        print(f"Admin liked article 1")
    
    dislike1, created = ArticleLike.objects.get_or_create(
        user=reader_user,
        article=article2,
        defaults={'is_like': False}
    )
    if created:
        print(f"Reader disliked article 2")
    
    bookmark1, created = BookmarkedArticle.objects.get_or_create(
        user=reader_user,
        article=article2
    )
    if created:
        print(f"Reader bookmarked article 2")
    
    bookmark2, created = BookmarkedArticle.objects.get_or_create(
        user=admin_user,
        article=article1
    )
    if created:
        print(f"Admin bookmarked article 1")
    
    print("\nTest data created successfully!")
    print(f"Article 1 - Likes: {article1.like_count}, Dislikes: {article1.dislike_count}, Views: {article1.views}")
    print(f"Article 2 - Likes: {article2.like_count}, Dislikes: {article2.dislike_count}, Views: {article2.views}")
    print(f"Reader's bookmarks: {reader_user.bookmarked_articles.count()}")
    print(f"Admin's bookmarks: {admin_user.bookmarked_articles.count()}")

if __name__ == '__main__':
    create_test_data()

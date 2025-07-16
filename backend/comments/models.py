from django.db import models
from articles.models import Article
from users.models import User


class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    user_name = models.CharField(max_length=100, blank=True)
    user_email = models.EmailField(blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username if self.user else self.user_name} on {self.article.title}'

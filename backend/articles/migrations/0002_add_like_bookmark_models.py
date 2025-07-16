# Generated migration for adding like/dislike and bookmark functionality

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),  # Replace with your latest migration
        ('users', '0001_initial'),  # Replace with your latest migration
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_likes', to='articles.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_likes', to='users.user')),
            ],
            options={
                'db_table': 'article_likes',
            },
        ),
        migrations.CreateModel(
            name='BookmarkedArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_by', to='articles.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_articles', to='users.user')),
            ],
            options={
                'db_table': 'bookmarked_articles',
            },
        ),
        migrations.AlterUniqueTogether(
            name='articlelike',
            unique_together={('user', 'article')},
        ),
        migrations.AlterUniqueTogether(
            name='bookmarkedarticle',
            unique_together={('user', 'article')},
        ),
    ]

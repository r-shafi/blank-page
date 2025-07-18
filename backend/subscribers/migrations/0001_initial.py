# Generated by Django 5.2 on 2025-07-15 15:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('subscription_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('unsubscribed', 'Unsubscribed')], default='active', max_length=20)),
                ('confirmation_token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('last_email_sent', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subscribers',
                'ordering': ['-subscription_date'],
            },
        ),
    ]

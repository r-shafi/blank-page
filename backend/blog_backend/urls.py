"""
URL configuration for blog_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/', include('admin_api.urls')),
    path('api/', include('core.urls')),
    path('api/users/', include('users.urls')),
    path('api/articles/', include('articles.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/subscribers/', include('subscribers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

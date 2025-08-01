from django.urls import path
from .views import (
    ArticleListCreateView,
    ArticleRetrieveUpdateDestroyView,
    ArticlePublishView,
    ArticleUnpublishView,
    ArticleBySlugView,
    PopularArticlesView,
    RecentArticlesView,
    RelatedArticlesView,
    IncrementViewsView,
    ImageUploadView,
    UserArticlesView,
    AdminArticleListAPIView,
    ArticleLikeView,
    ArticleBookmarkView,
    UserBookmarksView,
    UserLikedArticlesView,
    UserDislikedArticlesView,
)

urlpatterns = [
    path('', ArticleListCreateView.as_view(), name='article-list-create'),
    path('me/', UserArticlesView.as_view(), name='user-articles'),
    path('me/bookmarks/', UserBookmarksView.as_view(), name='user-bookmarks'),
    path('me/liked/', UserLikedArticlesView.as_view(), name='user-liked'),
    path('me/disliked/', UserDislikedArticlesView.as_view(), name='user-disliked'),
    path('popular/', PopularArticlesView.as_view(), name='popular-articles'),
    path('recent/', RecentArticlesView.as_view(), name='recent-articles'),
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),
    path('<int:pk>/related/', RelatedArticlesView.as_view(),
         name='related-articles'),
    path('<int:pk>/increment-views/',
         IncrementViewsView.as_view(), name='increment-views'),
    path('<slug:slug>/', ArticleRetrieveUpdateDestroyView.as_view(),
         name='article-detail'),
    path('<slug:slug>/like/', ArticleLikeView.as_view(), name='article-like'),
    path('<slug:slug>/bookmark/', ArticleBookmarkView.as_view(), name='article-bookmark'),
    path('<slug:slug>/publish/', ArticlePublishView.as_view(),
         name='article-publish'),
    path('<slug:slug>/unpublish/', ArticleUnpublishView.as_view(),
         name='article-unpublish'),
    path('by-slug/<slug:slug>/', ArticleBySlugView.as_view(), name='article-by-slug'),
    path('admin/', AdminArticleListAPIView.as_view(), name='article_admin_list'),
]

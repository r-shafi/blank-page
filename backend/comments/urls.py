from django.urls import path
from . import views

urlpatterns = [
    path('article/<int:article_id>/',
         views.CommentListView.as_view(), name='comment_list'),
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('<int:pk>/approve/', views.CommentApproveView.as_view(),
         name='comment_approve'),
    path('<int:pk>/reject/', views.CommentRejectView.as_view(),
         name='comment_reject'),
    path('pending/', views.PendingCommentsView.as_view(), name='pending_comments'),
    path('recent/', views.RecentCommentsView.as_view(), name='recent_comments'),
]

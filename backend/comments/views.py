from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(
            article_id=self.kwargs['article_id'],
            parent=None,
            status='approved'
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class CommentApproveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.status = 'approved'
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentRejectView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.status = 'rejected'
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class PendingCommentsView(generics.ListAPIView):
    queryset = Comment.objects.filter(status='pending')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


class RecentCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(status='approved').order_by('-created_at')[:10]

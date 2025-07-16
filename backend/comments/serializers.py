from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


class RecursiveCommentSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CommentSerializer(value)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'article', 'user', 'user_name', 'user_email', 'content',
                  'created_at', 'status', 'parent', 'replies')
        read_only_fields = ('id', 'created_at', 'status')
        extra_kwargs = {
            'user_name': {'required': False},
            'user_email': {'required': False},
            'parent': {'write_only': True}
        }

    def validate(self, attrs):
        if not attrs.get('user') and not (attrs.get('user_name') and attrs.get('user_email')):
            raise serializers.ValidationError(
                "Either user must be authenticated or both name and email must be provided")
        return attrs

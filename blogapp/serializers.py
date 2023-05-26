from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Comment, LikeDislike, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'body', 'created_at')
        model = Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'reviewed', 'parent',)


class PostAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email",)


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug",)


class PostApiCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'video', 'category',)


class PostApiListSerializers(serializers.ModelSerializer):
    author = PostAuthorSerializer()
    category = PostCategorySerializer()
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'title', 'slug', 'body', 'category', 'author', 'comments', 'likes',
            'dislikes',)

        # read_only_fields = ("category", "author",)


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'author', 'parent')
        read_only_fields = ("id", "post", "author", "parent",)


class PostLikeDislikeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=LikeDislike.LikeType.choices)


class PostLikeDislikeListSerializer(serializers.ModelSerializer):
    post = PostApiListSerializers(read_only=True)

    class Meta:
        model = LikeDislike
        fields = ('id', 'type', 'post',)

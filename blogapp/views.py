from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pagination import CustomPageNumberPagination
from .serializers import PostSerializer, UserSerializer, AddCommentSerializer, PostLikeDislikeSerializer, \
    PostLikeDislikeListSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, get_object_or_404, \
    ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Post, Comment, LikeDislike
from .permissions import IsAuthorOrReadOnly


# Create your views here.
# 1-option
class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserList(ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


# 2-option
# class PostViewSet(ModelViewSet):
#     permission_classes = (IsAuthorOrReadOnly,)
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class UserViewSet(ModelViewSet):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer

class AddCommentAPI(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_class = (IsAuthenticated,)
    lookup_field = 'slug'

    def perform_create(self, serializers):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        serializers.save(post=post, author=self.request.user)


class CommentDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            pk = self.kwargs.get("pk")
            comment = get_object_or_404(Comment, pk=pk)
            if comment:
                reviewed = self.queryset.values('reviewed').get(pk=pk)
                reviews = reviewed.get("reviewed")
                reviews += 1
                self.queryset.values('reviewed').filter(pk=pk).update(reviewed=reviews)
        return self.retrieve(request, *args, **kwargs)


class PostLikeApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PostLikeDislikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PostLikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_ = serializer.validated_data.get("type")
        user = request.user
        post = Post.objects.filter(slug=self.kwargs.get("slug")).first()
        if not post:
            raise Http404
        like = LikeDislike.objects.all()
        if like.filter(type=type_):
            like.delete()
            data = {"type": type_, "detail": "delete."}
            return Response(data)

        else:
            LikeDislike.objects.update_or_create(post=post, user=user, defaults={"type": type_})
            if type_ == 1:
                data = {"type": type_, "detail": "Liked."}
                return Response(data)
            elif type_ == -1:
                data = {"type": type_, "detail": "DisLiked."}
                return Response(data)


class LikeDislikeListApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    serializer_class = PostLikeDislikeListSerializer
    queryset = LikeDislike.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = get_object_or_404(self.queryset, user_id=request.user.id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

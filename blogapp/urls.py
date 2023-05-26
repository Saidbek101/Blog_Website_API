from django.urls import path
from .views import PostList, PostDetail, UserList, UserDetail, LikeDislikeListApi, PostLikeApiView, AddCommentAPI, \
    CommentDetailApi

urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('', PostList.as_view()),
    path('likedislike/', LikeDislikeListApi.as_view(), name='like_dislike-list'),
    path('blog/<slug:slug>/likedislike/', PostLikeApiView.as_view(), name='like_dislike'),
    path('blog/<slug:slug>/comment/', AddCommentAPI.as_view(), name='comment-add'),
    path('comment/<int:pk>/', CommentDetailApi.as_view(), name='comment-detail'),
]

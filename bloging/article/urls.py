from django.urls import path
from .views import (
    CreateArticleAPIView,
    ListArticleAPIView,
    DetailArticleAPIView,
    ListCommentAPIView,
    CreateCommentAPIView,
    ListCommentAPIView,
    DetailCommentAPIView
    )

app_name="article"
urlpatterns = [
    path("", ListArticleAPIView.as_view(), name="list_article"),
    path("create/", CreateArticleAPIView.as_view(), name="create_post"),
    path("<str:slug>/", DetailArticleAPIView.as_view(), name="post_detail"),
    path("<str:slug>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path(
        "<str:slug>/comment/create/",
        CreateCommentAPIView.as_view(),
        name="create_comment",
    ),
    path(
        "<str:slug>/comment/<int:id>/",
        DetailCommentAPIView.as_view(),
        name="comment_detail",
    ),
]
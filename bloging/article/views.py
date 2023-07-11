from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from rest_framework.response import Response

from .models import Article, Comments
from rest_framework.views import APIView

from .pagination import ArticleLimitOffsetPagination
from .serializers import (
    ArticleCreateUpdateSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CommentCreateUpdateSerializer,
)

from .permissions import IsOwnerOrReadOnly, IsOwner
from .mixins import MultipleFieldLookupMixin

# Create your views here.
class CreateArticleAPIView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = ArticleCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
class ListArticleAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ArticleLimitOffsetPagination

class DetailArticleAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = "slug"
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class CreateCommentAPIView(APIView):
    # parameters: [slug, body]
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Article, slug=slug)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent=post)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)
        
class ListCommentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        Article = Article.objects.get(slug=slug)
        comments = Comments.objects.filter(parent=Article)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)
    

class DetailCommentAPIView(MultipleFieldLookupMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a comment instance. Searches comment using comment id and post slug in the url.

    put:
        Updates an existing comment. Returns updated comment data

        parameters: [parent, author, body]

    delete:
        Delete an existing comment

        parameters: [parent, author, body]
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    queryset = Comments.objects.all()
    lookup_fields = ["parent", "id"]
    serializer_class = CommentCreateUpdateSerializer
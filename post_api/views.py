from rest_framework import generics, permissions
from post.models import Post, Category, Tag
from .serializers import PostSerializer, TagSerializer, CategorySerializer, SinglePostReadSerializer, SinglePostUpdateSerializer
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from .pagination import LargePagination
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

class PostListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminUserOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser] # parser
    queryset = Post.objects.filter(status = 'published').prefetch_related('category', 'author', 'tags')
    pagination_class = LargePagination

    def perform_create(self, serializer):
        user = User.objects.get( id = self.request.user.pk)
        serializer.validated_data['author'] = user
        serializer.save()


class SinglePostRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.prefetch_related('category', 'author', 'tags','comments')
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SinglePostUpdateSerializer 
        else:
            return SinglePostReadSerializer


    def perform_update(self, serializer):
        """
        You cannot change the owner of the post.
        """
        user = User.objects.get( id = self.request.user.pk)
        serializer.validated_data['author'] = user
        # print(serializer.validated_data)
        # print(self.request.method)
        serializer.save()


class SearchPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = LargePagination

    def get_queryset(self):
        queryset = Post.objects.prefetch_related('category', 'author', 'tags')
        author = self.request.query_params.get('author')
        tag = self.request.query_params.get('tag')
        category = self.request.query_params.get('category')
        title = self.request.query_params.get('title')

        if author is not None:
            queryset = queryset.filter(author__username__icontains=author)
        if tag is not None:
            queryset = queryset.filter(tags__title__icontains=tag)
        if category is not None:
            queryset = queryset.filter(category__title__icontains=category)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title) | Q(excerpt__icontains=title))
            
        return queryset


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related()


class TagListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = TagSerializer
    queryset = Tag.objects.select_related()


class CategoryPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(category__pk = self.kwargs.get('category_pk')).prefetch_related('category', 'author', 'tags')


class TagPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(tags__pk = self.kwargs.get('tag_pk')).prefetch_related('category', 'author', 'tags')



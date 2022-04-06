from rest_framework import generics
from post.models import Post, Category, Tag
from .serializers import PostSerializer, TagSerializer, CategorySerializer
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrReadOnly
from rest_framework.exceptions import ValidationError
from .pagination import LargePagination, SmallPagination
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User


class PostListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser] # Form içerisinden image alanına izin ver
    queryset = Post.objects.filter(status = 'published').prefetch_related('category', 'author', 'tags')
    pagination_class = LargePagination

    def perform_create(self, serializer):
        user = User.objects.get( id = self.request.user.pk)
        serializer.validated_data['author'] = user
        serializer.save()


class SinglePostRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        """
        You cannot change the owner of the post.
        """
        # Author alanını isteğe dahil bile etmedik bu şekilde
        user = User.objects.get( id = self.request.user.pk)
        serializer.validated_data['author'] = user
        
        # print(serializer.validated_data)
        # post_pk = self.kwargs.get('pk')
        # post = Post.objects.get(pk = post_pk)
        # if post.author.pk != int(self.request.data['author']):
        #     raise ValidationError('Postun sahibini değiştiremezsiniz.')
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
            queryset = queryset.filter(tags__title=tag)
        if category is not None:
            queryset = queryset.filter(category__title__icontains=category)
        if title is not None:
            queryset = queryset.filter(Q(title__icontains=title) | Q(excerpt__icontains=title))
            
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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
        print('Girdi')
        return Post.objects.filter(category__pk = self.kwargs.get('category_pk')).prefetch_related('category', 'author', 'tags')


class TagPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.filter(tags__pk = self.kwargs.get('tag_pk')).prefetch_related('category', 'author', 'tags')



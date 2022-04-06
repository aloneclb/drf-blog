from django.urls import path
from . import views as api_view


app_name = 'post_api'

urlpatterns = [
    path('', api_view.PostListCreateView.as_view(), name='postlistcreate'),

    path('get/post/<int:pk>/', api_view.SinglePostRetrieveDestroyView.as_view(), name='postdetailcreate'),

    path('get/category/', api_view.CategoryListView.as_view(), name='categorylistcreate'),

    path('get/category/<int:category_pk>/', api_view.CategoryPostListView.as_view(), name='categorypostlist'),

    path('get/tag/', api_view.TagListView.as_view(), name='taglistcreate'),

    path('get/tag/<int:tag_pk>/', api_view.TagPostListView.as_view(), name='tagpostlist'),

    path('search/', api_view.SearchPostListView.as_view(), name='searchlist' ),

]
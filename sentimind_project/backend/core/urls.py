from django.urls import path
from core.infrastructure.views import PostListCreateView, CategoryListView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]

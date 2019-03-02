from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

#empty '' means home maps to home funtion in view file
urlpatterns = [
    path('', views.home, name='blog-home'),
    path('millitaryacronyms/', views.m_a, name='blog-m_a'),
    path('FAQ/', views.FAQ, name='blog-FAQ'),
    path('guestbook/', PostListView.as_view(), name='blog-guestbook'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    #pk is primary key, post/1 is first post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
]
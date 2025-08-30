from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('u/<str:username>/', views.profile_view, name='profile'),
    path('u/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('settings/profile/', views.profile_edit, name='profile_edit'),
]

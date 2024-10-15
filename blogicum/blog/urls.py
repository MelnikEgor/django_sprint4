from django.urls import include, path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path(
        'category/<slug:category_slug>/',
        views.CatgoryView.as_view(),
        name='category_posts'
    ),
    path('posts/', include('blog.posts_urls')),
    path(
        'profile/edit/',
        views.UserUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
]

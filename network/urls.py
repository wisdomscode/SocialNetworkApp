
from django.urls import path

from . import views
from .views import HomeView, CreatePost, UpdatePost, DeletePost

urlpatterns = [
   path("login", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register/", views.register, name="register"),

   # path("", views.index, name="index"),
   path('', HomeView.as_view(), name="index"),
   path('post/create/', CreatePost.as_view(), name="create_post"),
   path('post/update/', UpdatePost.as_view(), name="update_post"),
   path('post/delete/', DeletePost.as_view(), name="delete_post"),
   
   path("like_post/", views.like_unlike_post, name="like-post-view"),
   path("following/", views.following_user, name="following-user"),
   path("users/following/", views.users_following, name="users-following"),

   path("<int:page_user_id>/profile", views.show_profile, name='show_profile'),
   path("<int:user_id>/edit_profile", views.edit_profile, name='edit_profile'),

] 

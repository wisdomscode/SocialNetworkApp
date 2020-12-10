from django.contrib import admin
from .models import UserProfile, Post, Like, Following



class PostAdmin(admin.ModelAdmin):
  list_display = ("poster", "body", "post_date")

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ("id", "user", "gender")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Following)
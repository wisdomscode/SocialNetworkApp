from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date

# Create your models here.
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   location = models.CharField(max_length=30)
   gender = models.CharField(max_length=255, null=True, blank=True)
   profile_pic = models.ImageField(null=True, blank=True, upload_to='profile/')
   following = models.ManyToManyField(User, related_name="following_user", blank=True, symmetrical=False)

   def __str__(self):
      return str(self.user)

   def num_following(self):
      return self.following.all().count()
   


FOLLOW_CHOICES = (
    ('Follow', 'Follow'),
    ('Unfollow', 'Unfollow'),
)
class Following(models.Model):
   followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed",)
   followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers",)
   value = models.CharField(choices=FOLLOW_CHOICES, max_length=15)
   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
      return f"{self.user}-{self.value}"





class Post(models.Model):
   poster = models.ForeignKey(User, on_delete=models.CASCADE)
   body = models.TextField(blank=True, null=True)
   post_date = models.DateTimeField(auto_now_add=True)
   liked = models.ManyToManyField(User, related_name='like_post', blank = True)
   
   class Meta:
      ordering = ['-post_date']

   def __str__(self):
      return str(self.poster)

   def num_likes(self):
      return self.liked.all().count()



LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   value = models.CharField(choices=LIKE_CHOICES, max_length=8)
   updated = models.DateTimeField(auto_now=True)
   created = models.DateTimeField(auto_now_add=True)
    
   def __str__(self):
      return f"{self.user}-{self.post}-{self.value}"


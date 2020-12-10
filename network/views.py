from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .forms import ExtendedUserCreationForm, UserProfileForm, PostForm, EditProfileForm
 
from .models import Post, UserProfile, Like, Following
from django.contrib.auth.models import User

from django.views import generic
from django.views.generic import ListView, View

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def login_view(request):
    if request.method == "POST":

      # Attempt to sign user in
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(request, username=username, password=password)

      # Check if authentication successful
      if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
      else:
        return render(request, "network/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
      return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
   if request.method == "POST":
      form = ExtendedUserCreationForm(request.POST)
      profile_form = UserProfileForm(request.POST, request.FILES)

      if form.is_valid() and profile_form.is_valid():
         user = form.save()

         profile = profile_form.save(commit=False)
         profile.user = user

         profile.save()

         username = form.cleaned_data['username']
         password = form.cleaned_data['password1']
         user = authenticate(username=username, password=password)
         login(request, user)
         return redirect('index')
   else:
      form = ExtendedUserCreationForm()
      profile_form = UserProfileForm()

      context = { 'form':form, 'profile_form':profile_form }
   return render(request, 'network/register.html', context)
   

def edit_profile(request, user_id):
   user = User.objects.get(id=user_id)
   pro_user = UserProfile.objects.get(id=user_id)
   form = EditProfileForm(instance=user)
   profile_form = UserProfileForm(instance=pro_user)
   if request.method == "POST":
      form = EditProfileForm(request.POST)
      profile_form = UserProfileForm(request.POST, request.FILES)
      if form.is_valid() and profile_form.is_valid():
         user = form.save()
         profile = profile_form.save(commit=False)
         profile.user = user
         profile.save()
         
         return HttpResponseRedirect(reverse("index"))
   context = { 'form':form, 'profile_form':profile_form }
   return render(request, 'network/edit_profile.html', context)
  

  ######################################################

# def index(request):
#    posts = Post.objects.all()
#    return render(request, "network/index.html", {"posts":posts})

class HomeView(ListView):
   model = Post
   template_name = 'network/index.html'
   context_object_name = 'posts'
   ordering = ['-post_date']
   paginate_by = 10
   queryset = Post.objects.all()



class CreatePost(View):
   def get(self, request):
      poster1 = request.GET.get('poster', None)
      user = get_object_or_404(User, pk=poster1)
      body1 = request.GET.get('body', None)

      obj = Post.objects.create(
         poster = user,
         body = body1
      )
      # user1 = obj.poster.username

      # date = obj.post_date.strftime("%c")
      date = obj.post_date.strftime("%b %-d %Y, %-I:%M %p")
      post = {'id':obj.id,'poster':obj.poster.username,'post_date':date,'body':obj.body}
      data = {
         'post': post
      }
      return JsonResponse(data)


class UpdatePost(View):
   def  get(self, request):
      id1 = request.GET.get('id', None)
      body1 = request.GET.get('body', None)

      obj = Post.objects.get(id=id1)
      obj.body = body1
      obj.save()

      # date = obj.post_date.strftime("%c")
      # date = obj.post_date.strftime("%b %-d %Y, %-I:%M %p")
      post = {'id':obj.id, 'body':obj.body}

      data = {
         'post': post
      }
      return JsonResponse(data)


class DeletePost(View):
   def  get(self, request):
      id1 = request.GET.get('id', None)
      Post.objects.get(id=id1).delete()
      data = {
         'deleted': True
      }
      return JsonResponse(data)

    

def show_profile(request, page_user_id):
   page_user = UserProfile.objects.get(id=page_user_id)
   posts = Post.objects.filter(poster=page_user.user.id)

   # current_user = request.user

   # This shows all the people current user is following
   users_followed = UserProfile.objects.filter(following=page_user.id)
   num_followed = users_followed.count()

   page = request.GET.get('page', 1)

   paginator = Paginator(posts, 10)
   try:
      posts = paginator.page(page)
   except PageNotAnInteger:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)

   print(page_user)

   context = { "page_user":page_user, "posts":posts, "num_followed": num_followed}
   return render(request, "network/profile.html", context)



def like_unlike_post(request):
   user = request.user
   print(user)
   if request.method == 'POST':
      post_id = request.POST.get('post_id')
      post_obj = Post.objects.get(id=post_id)
      profile = User.objects.get(username=user)

      if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
      else:
            post_obj.liked.add(profile)

      like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

      if not created:
            if like.value=='Like':
               like.value='Unlike'
            else:
               like.value='Like'
      else:
            like.value='Like'

            post_obj.save()
            like.save()

      data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
      }

      return JsonResponse(data, safe=False)
   return redirect('index')



def following_user(request):
   user = request.user
   if request.method == 'POST':
      poster_id = request.POST.get('poster_id')
      poster = UserProfile.objects.get(id=poster_id)


      if user in poster.following.all():
            poster.following.remove(user)
      else:
            poster.following.add(user)

      follow, created = Following.objects.get_or_create(followed=user, followers=poster.user)

      if not created:
         if follow.value=='Follow':
            follow.value='Unfollow'
         else:
            follow.value='Follow'
      else:
            follow.value='Follow'

            poster.save()
            follow.save()

      data = {
         'value': follow.value,
         'following': poster.following.all().count()
      }     
      return JsonResponse(data, safe=False)

   return redirect('show_profile')



def users_following(request):
   current_user = request.user

   # This shows all the people current user is following
   users_followed = UserProfile.objects.filter(following=current_user.id)
   n_users_followed = users_followed.count()

   followed_users = users_followed.values_list('user_id', flat=True).order_by('id')

   posts = Post.objects.filter(poster__in=followed_users)

   # This shows all the people following current user
   # followers = current_user.userprofile.following.all()
   # n_followers = current_user.userprofile.following.all().count()

   page = request.GET.get('page', 1)

   paginator = Paginator(posts, 10)
   try:
      posts = paginator.page(page)
   except PageNotAnInteger:
      posts = paginator.page(1)
   except EmptyPage:
      posts = paginator.page(paginator.num_pages)

   context = {"posts":posts}
   return render(request, "network/following.html", context)


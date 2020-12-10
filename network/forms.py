from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, Post
from django.forms import ModelForm


class ExtendedUserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
  first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
  last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


  username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  
  class Meta:
    model =  User
    fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)

 

  def save(self, commit=True):
    user = super().save(commit=False)

    user.email = self.cleaned_data['email']
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']

    if commit:
      user.save()
    return user


gender_list = [('Male','Male'), ('Female','Female')]

class UserProfileForm(forms.ModelForm):
   class Meta:
      model = UserProfile
      fields = ('location', 'gender', 'profile_pic')

      widgets = {
         'location': forms.TextInput(attrs={'class': 'form-control'}),
         'gender': forms.Select(choices=gender_list, attrs={'class': 'form-control'}),
         'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
         
      }


class EditProfileForm(UserChangeForm):
   username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   email =  forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
   first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

   class Meta:
      model = User
      fields = ('username', 'email', 'first_name', 'last_name')




class PostForm(ModelForm):
   class Meta:
      model = Post
      fields = ('poster', 'body')

      widgets =  {
         'poster': forms.TextInput(attrs={'class': 'form-control', 'id':'poster', 'value':'', 'type':'hidden'}),
         'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your post here', 'rows':5}),
      }


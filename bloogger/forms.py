from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class AdminCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_admin=True
        if commit:
            user.save()
        return user
    
class PrivateCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
    def save(self,commit=True):
        user = super().save(commit=False)
        user.is_private=True
        if commit:
            user.save()
        return user
    
class PublicCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_public=True
        if commit:
            user.save()
        return user

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields="__all__"

class PostCreateForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude = ("author",)

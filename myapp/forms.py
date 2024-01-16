from django import forms

from myapp.models import Books
from django.contrib.auth.models import User

class BooksModelForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={
            "isbn":forms.NumberInput(attrs={"class":"form-control mt-2"}),
            "book_name":forms.TextInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "publisher":forms.TextInput(attrs={"class":"form-control"}),
            "published_year":forms.NumberInput(attrs={"class":"form-control"})
        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","password","email"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control mt-3"}),
            "password":forms.PasswordInput(attrs={"class":"form-control mt-3"}),
            "email":forms.EmailInput(attrs={"class":"form-control mt-3"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-3"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-3"}))

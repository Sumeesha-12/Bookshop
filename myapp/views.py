from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View
from myapp.models import Books
from myapp.forms import BooksModelForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid session")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,"dispatch")
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BooksModelForm()
        return render(request,"book_create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=BooksModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Book added successfully")
            print("created")
            return render(request,"book_create.html",{"form":form})
        else:
            messages.error(request,"Failed to add book")
            return render(request,"book_create.html",{"form":form})
@method_decorator(signin_required,"dispatch")  
class BookListView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        author=Books.objects.all().values_list("author",flat=True).distinct()

        if "author" in request.GET:
            auth=request.GET.get("author")
            qs=qs.filter(author__iexact=auth)

        return render(request,"book_list.html",{"data":qs,"author":author})
    
    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Books.objects.filter(book_name__icontains=name)
        return render(request,"book_list.html",{"data":qs})

@method_decorator(signin_required,"dispatch")
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"book_detail.html",{"data":qs})


@method_decorator(signin_required,"dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        messages.success(request,"Book deletion success")
        return redirect("book-list")


@method_decorator(signin_required,"dispatch")
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BooksModelForm(instance=obj)
        return render(request,"book_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BooksModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Book changes updated")
            return redirect("book-detail",pk=id)
        else:
            messages.error(request,"Failed to update book")
            return render(request,"book_edit.html",{"form":form})
        

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Registered Successfully")
            return render(request,"register.html",{"form":form})

        else:
            messages.error(request,"Failed")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")

            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid credentials")
                login(request,user_obj)
                return redirect("book-list")
            
            messages.error(request,"InValid Credentials")
            return render(request,"login.html",{"form":form})
                

@method_decorator(signin_required,"dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")

            
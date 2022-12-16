from django.shortcuts import render, redirect
from django.views.generic import View,TemplateView
from todoweb.form import UserRegistrationForm, UserLoginForm,TodoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from todolist.models import Todos
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kw):
        if not request.user.is_authenticated:
            messages.error(request,"You must login first")
            return redirect("signin")
        else:
            return fn(request,*args,**kw)
    return wrapper

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form":form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"your account has been created")
            return redirect("signin")
        else:
            return render(request, "register.html", {"form":form})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, "login.html", {"form":form})

    def post(self,request,*args,**kw):
        form= UserLoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"Login Successful")
                return redirect("home")
            else:
                messages.error(request,"Invalid User")
                print("Invalid User")
                return redirect("signin")

@method_decorator(signin_required,name="dispatch")
class IndexView(TemplateView):
    
    template_name="index.html"
    # def get(self,request,*args,**kw):
    #     return render(request,"index.html")

@method_decorator(signin_required,name="dispatch")
class TodoListView(View):
    def get(self,request,*args,**kw):
        qs=Todos.objects.filter(user=request.user)
        return render(request,"todo-list.html",{"todos":qs})

@method_decorator(signin_required,name="dispatch")
class TodoAddView(View):
    def get(self,request,*args,**kw):
        form=TodoForm()
        return render(request,"todo-add.html",{"form":form})

    def post(self,request,*args,**kw):
        form=TodoForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            return redirect("todo-list")
        else:
            return render(request,"todo-add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class TodoDetailView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        qs=Todos.objects.get(id=id)
        return render(request,"todo-details.html",{"todo":qs})

@signin_required
def todo_delete_view(request,*args,**kw):
    id=kw.get("id")
    Todos.objects.get(id=id).delete()
    return redirect("todo-list")


def sign_out(request,*args,**kw):
    logout(request)
    return redirect("signin")
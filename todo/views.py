from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import Todoform
from .models import Todo

def signupuser(request):
    if request.method == "GET":
        return render(request,"todo/signupuser.html", {"form":UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect ('currenttodo')

            except IntegrityError:
                return render(request,"todo/signupuser.html", {"form":UserCreationForm(), 'error':'Username not available, please choose another name'})
        else:
            return render(request,"todo/signupuser.html", {"form":UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == "GET":
        return render(request,"todo/loginuser.html", {"form":AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,"todo/loginuser.html", {"form":AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect ('currenttodo')            

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def create(request):
    if request.method == "GET":
        return render(request,"todo/create.html", {"form":Todoform()})
    else:
        try:
            form = Todoform(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,"todo/create.html", {"form":Todoform(), 'error':'Bad Data Pass In'})

def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request,'todo/currenttodo.html',{'todos':todos})

def home(request):
    return render(request,'todo/home.html')
    
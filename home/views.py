from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Todo

# Create your views here.


def home(request):
    todos = []
    if request.user.is_authenticated:
        todos = [todo for todo in Todo.objects.filter(user=request.user)]
        if request.POST:
            title = request.POST.get('todo')
            print(request.POST.get('todo'))
            todo = Todo.objects.create(user=request.user, title=title)
            todos.append(todo)
        return render(request, 'home.html', {'todos': todos})
    else:
        return redirect(signin)


def createTodo(request):
    if request.user.is_authenticated:
        print(request.POST.get("todo"))
        return redirect(home)
    else:
        return redirect(signin)


def updateTodoIsDone(request, id):
    if request.user.is_authenticated:
        todo = Todo.objects.get(id=id)
        if not todo.isDone:
            todo.isDone = True
        else:
            todo.isDone = False
        todo.save()
        return redirect(home)
    else:
        return HttpResponse("You are not authenticated!")


def todoDelete(request, id):
    if request.user.is_authenticated:
        todo = Todo.objects.get(id=id)
        todo.delete()
        return redirect(home)
    else:
        return HttpResponse("You are not authenticated!")


def signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            request.user = Profile.objects.filter(user=user)
            login(request, user)
            return redirect(home)
        else:
            return HttpResponse("Login Failed")

    else:
        return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profileImg = request.FILES.get("profile")
        # print(request.FILES.get("profile"))
        if User.objects.filter(username=username).exists():
            return HttpResponse("User already exists")
        elif User.objects.filter(email=email).exists():
            return HttpResponse("User already exists")
        else:
            try:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                Profile.objects.create(user=user, image=profileImg)
                # login(user)
                return redirect(home)
            except:
                HttpResponse("User not created , Try again")

        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')


def signout(request):
    logout(request)
    return redirect(signin)

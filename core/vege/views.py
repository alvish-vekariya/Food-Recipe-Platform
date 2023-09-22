from django.shortcuts import render, redirect
from .models import Receipe
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_page")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        rfile = request.FILES.get('image')
        rname = data.get('name')
        rdesc = data.get('desc')
        # print(rname)
        # print(rdesc)
        # print(rfile)

        Receipe.objects.create(name=rname, desc =rdesc, image=rfile)
        return redirect('/receipes')

    queryset = Receipe.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(name__icontains = request.GET.get('search'))

    context = {'receipes':queryset}

    return render(request, 'index.html',context)

def delete(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('receipes')

def update(request, id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        rfile = request.FILES.get('image')
        rname = data.get('name')
        rdesc = data.get('desc')

        queryset.name = rname
        queryset.desc = rdesc
        
        if rfile:
            queryset.image = rfile
        
        queryset.save()

        return redirect('receipes')


    context = {'receipes':queryset}
    return render(request, 'update_receipes.html',context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid User.')
            return redirect('login_page')

        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("receipes")

        else:
            # No backend authenticated the credentials
            messages.error(request, 'Invalid Password.')
            return redirect('login_page')

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login_page')

def register(request):
    if request.method=="POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')

        user = User.objects.filter(username = uname)

        if user.exists():
            messages.info(request, 'User already exists..')
            return redirect('register')

        user = User.objects.create(
            first_name = fname,
            last_name = lname,
            username = uname
        )

        user.set_password(pswd)
        user.save()
        messages.info(request,"account created successfully.")

        return redirect('register')

    return render(request, 'register.html')
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Profile,User
from django.contrib.auth import authenticate,login,logout

def auth(request):
    return render(request, 'auth.html')

def register(request):
    if request.method == 'POST':
        uname = request.POST['tel']
        pwd = request.POST['pwd']
        role = request.POST['role']
        print(uname)
        print(pwd)
        print(role)
        # User Creation
        usr = User.objects.create_user(username=uname,password=pwd)
        usr.save()
        pf = Profile(user = usr,phone_number = uname,role = role)
        pf.save()
        print(f"This is pf {pf}")
        return HttpResponse("Ok")
    return render(request,'auth.html')

def test(request):
    print(request.user)
    usr = request.user
    pf = Profile.objects.get(user = usr)
    print(pf)
    print(pf.role)
    return HttpResponse("request.user")

def login_user(request):
    if request.method == "POST":
        name = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(request,username=name,password = pwd)
        if user is not None:
            login(request,user)
            return redirect("/")
        

def index(request):
    pass
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
def account(request):
    if not request.user.is_authenticated:    
        return render(request,"home/login.html",{"message": "Enter username and password"})
    else:
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin')
        else:
            context = {
                "user": request.user
            }
            return render(request,'account/user.html',context)
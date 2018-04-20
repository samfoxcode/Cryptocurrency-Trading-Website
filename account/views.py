from django.shortcuts import render
from django.contrib.auth import authenticate
def account(request):
    if not request.user.is_authenticated:
        return render(request,'account/accountmain.html')
    context = {
        "user": request.user
    }
    return render(request,'account/user.html',context)
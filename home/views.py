from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    if request.method == 'GET':

        search_query = request.GET.get('search_box', None)
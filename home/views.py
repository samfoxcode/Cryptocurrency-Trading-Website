from django.shortcuts import render
from django.http import HttpResponse
from home.models import Coins, Tweets
from django.contrib.auth.models import User
from home.models import UserProfile
from home.models import UserForm, UserProfileForm
from django.shortcuts import render_to_response
from crypto_web.settings import MEDIA_ROOT
from django.template import RequestContext
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def signin(request):
    return render(request, 'home/signin.html')

def register(request):
    return render(request, 'home/register.html')

def contact(request):
    return render(request, 'home/contact.html')

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        status = Coins.objects.filter(coin_name=search_query)
        coins = {"coins": status} #true or false
        return render(request, 'home/index.html', coins)

def register(request):
        context = RequestContext(request)
        registered = False
        if request.method == 'POST':
                uform = UserForm(data = request.POST)
                pform = UserProfileForm(data = request.POST)
                if uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        profile = pform.save(commit = False)
                        profile.user = user
                        profile.firstname = pform.data['firstname']
                        profile.lastname = pform.data['lastname']
                        profile.save()
                        #save_file(request.FILES['picture'])
                        registered = True
                else:
                        print(uform.errors, pform.errors)
        else:
                uform = UserForm()
                pform = UserProfileForm()

        return render(request, 'home/register.html', {'uform': uform, 'pform': pform, 'registered': registered })


def save_file(file, path=''):
        filename = file._get_name()
        fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb' )
        for chunk in file.chunks():
                fd.write(chunk)
        fd.close()


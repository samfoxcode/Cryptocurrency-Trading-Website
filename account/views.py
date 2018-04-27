from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from home.models import Coins, Tweets, UserTransactions, UserBalance, UserProfile, UserTransactions_Time
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
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

def signedinhome(request):
    return render(request, 'account/signedinhome.html')

def about(request):
    return render(request, 'account/about.html')

def contact(request):
    return render(request, 'account/contact.html')

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        status = Coins.objects.filter(coin_name=search_query)
        ticker = Coins.objects.get(coin_name=search_query)
        tweets = Tweets.objects.filter(ticker=ticker.ticker).order_by('timestamp')[:5]
        coins = {'search': {"coins": status, "tweets":tweets}} #true or false
        return render(request, 'account/signedinhome.html', coins)

def logout_view(request):
        logout(request)
        return render(request,"home/login.html",{"message": "Logged out"})

def buy(request):
    curr_amount = 0
    if request.method == 'POST':
        print("hit")
        username = request.user
        buy_amount = request.POST.get('buy_box', "")
        ticker = request.POST.get('ticker_box', "")
        status = Coins.objects.filter(ticker=ticker)

        if(status.count() == 0):
            print("no coin")
            return render(request, 'account/signedinhome.html', {"no_coin": {"ticker": ticker}})

        status = Coins.objects.get(ticker=ticker)
        cost = float(status.current_price)*float(buy_amount)
        balance, created = UserBalance.objects.get_or_create(username=username, defaults={"balance": 0})

        if(float(balance.balance) - cost < 0):
            print("no_funds")
            return render(request, 'account/signedinhome.html', {"no_funds": {"ticker": ticker}})
        else:
            UserBalance.objects.filter(username=username).update(balance=float(balance.balance)-float(cost))

        transact = UserTransactions_Time(username=username, ticker=ticker, amount=buy_amount, timestamp= datetime.now())
        transact.save()
        transaction, created = UserTransactions.objects.get_or_create(username=username, ticker=ticker, defaults={"amount": buy_amount})
        if created:
            send_mail('PHF PHF TRANSACTION','You just bought ' + str(buy_amount) + " of " + ticker,'samf1596@gmail.com',['samf1596@gmail.com'],fail_silently=False,)
            return render(request, 'account/signedinhome.html', {"curr_amounts": {"amount": float(buy_amount), "ticker": ticker}})
        else:
            curr_amount = UserTransactions.objects.get(username=username, ticker=ticker)
            print(curr_amount)
            UserTransactions.objects.filter(username=username, ticker=ticker).update(amount=float(buy_amount)+float(curr_amount.amount))
            send_mail('PHF PHF TRANSACTION','You just bought ' + str(buy_amount) + " of " + ticker,'samf1596@gmail.com',['samf1596@gmail.com'],fail_silently=False,)
            return render(request, 'account/signedinhome.html', {"curr_amounts": {"amount": float(buy_amount)+float(curr_amount.amount), "ticker": ticker}})

def load_info(request):
    if request.method == 'GET':
        username = request.user
        holdings = UserTransactions.objects.filter(username=username)
        balance, created = UserBalance.objects.get_or_create(username=username, defaults={"balance": 0})
        user, created2 = UserProfile.objects.get_or_create(user=username)
        transactions = UserTransactions_Time.objects.filter(username=username).order_by('timestamp')[:5]
        print(balance.balance)
        return render(request, 'account/user.html', {"info": {"holding": holdings, "balances":balance, "user":user.creditcard%10000, "transactions":transactions}})

def sell(request):
    if request.method == 'POST':
        username = request.user
        sell_amount = request.POST.get('buy_box', "")
        ticker = request.POST.get('ticker_box', "")
        
        status = Coins.objects.filter(ticker=ticker)
        if(status.count() == 0):
            pass
        else:
            status = Coins.objects.get(ticker=ticker)
            cost = float(status.current_price)*float(sell_amount)
        balance, created = UserBalance.objects.get_or_create(username=username, defaults={"balance": 0})
        UserBalance.objects.filter(username=username).update(balance=float(balance.balance)+float(cost))

        if(UserTransactions.objects.filter(username=username, ticker=ticker).count()<=0):
            return render(request, 'account/signedinhome.html', {"do_not_own": {"ticker": ticker}})

        transact = UserTransactions_Time(username=username, ticker=ticker, amount=sell_amount, timestamp= datetime.now())
        transact.save()
        curr_amount = UserTransactions.objects.get(username=username, ticker=ticker)
        print(curr_amount)
        if(float(curr_amount.amount)-float(sell_amount) < 0):
            sell_amount = float(curr_amount.amount) # will result in selling all
            UserTransactions.objects.filter(username=username, ticker=ticker).update(amount=float(curr_amount.amount)-float(sell_amount))
            send_mail('PHF PHF TRANSACTION','You just sold all of your ' + str(ticker),'samf1596@gmail.com',['samf1596@gmail.com'],fail_silently=False,)
            return render(request, 'account/signedinhome.html', {"sold_all": {"ticker": ticker}})

        UserTransactions.objects.filter(username=username, ticker=ticker).update(amount=float(curr_amount.amount)-float(sell_amount))
        send_mail('PHF PHF TRANSACTION','You just sold ' + str(sell_amount) + " of " + ticker,'samf1596@gmail.com',['samf1596@gmail.com'],fail_silently=False,)
        return render(request, 'account/signedinhome.html', {"curr_amounts": {"amount": float(curr_amount.amount) - float(sell_amount), "ticker": ticker}})

def update_balance(request):
    if request.method == "POST":
        username = request.user
        balance = request.POST.get('balance_box', "")
        send_mail('PHF PHF TRANSACTION','Thank you for depositing ' + str(balance) + ' into your account!','samf1596@gmail.com',['samf1596@gmail.com'],fail_silently=False,)
        user, created2 = UserProfile.objects.get_or_create(user=username)
        holdings = UserTransactions.objects.filter(username=username)
        transaction, created = UserBalance.objects.get_or_create(username=username, defaults={"balance": balance})
        if created:
            balance = UserBalance.objects.get(username=username)
            return render(request, 'account/user.html', {"info": {"holding": holdings, "balances":balance, "user":user.creditcard%10000}})

        print(transaction.balance)
        UserBalance.objects.filter(username=username).update(balance=float(balance)+float(transaction.balance))
        balance = UserBalance.objects.get(username=username)
        return render(request, 'account/user.html', {"info": {"holding": holdings, "balances":balance, "user":user.creditcard%10000}})

def contact_email(request):
    if request.method == "POST":
        text = request.POST.get('comments', "")
        sender = request.POST.get('email', "")
        name = request.POST.get('name', "")
        send_mail('Customer Email', name + " says " + str(text) ,sender,['samf1596@gmail.com'],fail_silently=False,)
        return render(request, 'account/contact.html', {"email_sent": {"sent": 1234}})
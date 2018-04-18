from django.db import models
from django.forms import ModelForm

import os
import django
import crypto_web
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_web.settings")
django.setup()
from django.contrib.auth.models import User
class UserProfile(models.Model):
        # This field is required.
        user = models.OneToOneField(User, on_delete=models.PROTECT)
        # These fields are optional
        website = models.URLField(blank=True)
        picture = models.ImageField(upload_to='imgs', blank=True)

        def __unicode__(self):
                return self.user.username

class Coins(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    coin_name = models.CharField(max_length=10)
    website = models.CharField(max_length=30)
    current_price = models.DecimalField(decimal_places=3, max_digits=12)
    gain_loss = models.DecimalField(decimal_places=3, max_digits=12)
    
    def __str__(self):
        return self.ticker

class Tweets(models.Model):
    ticker = models.CharField(max_length=10)
    text = models.CharField(max_length=50)
    sentiment = models.DecimalField(decimal_places=2, max_digits=12)
    current_price = models.DecimalField(decimal_places=2, null=False, max_digits=12)
    timestamp = models.DateTimeField()
    class Meta:
        #Our "primary" key for tweets
        unique_together = (('ticker', 'timestamp'),)

    def __str__(self):
        return self.ticker

class Old_Prices(models.Model):
    timestamp = models.DateTimeField()
    ticker = models.ForeignKey(Coins, on_delete=models.PROTECT) #don't cascade on delete, still important
    accuracy_projection = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=3, max_digits=12)

    class Meta:
        #Our "primary" key for old_prices
        unique_together = (('ticker', 'timestamp'),)

    def __str__(self):
        return (self.timestamp, self.ticker)

class UserForm(ModelForm):
        class Meta:
                model = User
                fields = ["username", "email", "password"]

class UserProfileForm(ModelForm):
        class Meta:
                model = UserProfile
                fields = ['website','picture']

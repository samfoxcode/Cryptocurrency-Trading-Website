from django.db import models
from mongoengine import *
from django_mongoengine import Document, EmbeddedDocument, fields
import os
import django
import crypto_web

connect('431')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crypto_web.settings")
django.setup()
m

class Coins(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    website = models.CharField(max_length=30)
    current_price = models.DecimalField(decimal_places=3, max_digits=12)
    gain_loss = models.DecimalField(decimal_places=3, max_digits=12)

    def __str__(self):
        return self.ticker


class Tweets(models.Model):
    ticker = models.ForeignKey(Coins, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    sentiment = models.DecimalField(decimal_places=2, max_digits=12)
    current_price = models.DecimalField(decimal_places=2, null=False, max_digits=12)

    def __str__(self):
        return self.ticker


class Old_Prices(models.Model):
    timestamp = models.DateTimeField()
    ticker = models.ForeignKey(Coins, on_delete=models.PROTECT)  # don't cascade on delete, still important
    accuracy_projection = models.DecimalField(decimal_places=2, max_digits=12)
    price = models.DecimalField(decimal_places=3, max_digits=12)

    class Meta:
        # Our "primary" key for old_prices
        unique_together = (('ticker', 'timestamp'),)

    def __str__(self):
        return self.timestamp, self.ticker


class Address(EmbeddedDocument):
    street = StringField(max_length=200)
    city = StringField(max_length=200)
    state_province = StringField(max_length=200)
    zip_postal = IntField(max_value=999999)
    country = StringField(max_length=200)


class Users(Document):
    first_name = StringField(max_length=200)
    last_name = StringField(max_length=200)
    email = EmailField()
    birthday = DateTimeField()
    address = ListField(EmbeddedDocumentField(Address))
    phone_number = LongField(max_value=9999999999)
    ssn = LongField(primary_key=True, max_value=9999999999)
    country = StringField(max_length=200)


class Account(Document):
    username = StringField(max_length=20, primary_key=True)
    password = StringField(max_length=40)


class Credit_card(Document):
    card_num = LongField(min_value=0000000000000000, max_value=9999999999999999, primary_key=True)
    ccv = IntField(min_value=000, max_value=999, primary_key=True)
    bank_name = StringField(max_length=50)
    owner_name = StringField(max_length=200)

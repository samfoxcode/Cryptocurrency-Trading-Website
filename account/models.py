from djongo import models


class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    zip_postal = models.IntegerField(max_length=10)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True


class cardOwnerName(models.Model):
    first_name = models.CharField(null=False)
    last_name = models.CharField(null=False)

    class Meta:
        abstract = True


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ssn = models.BigIntegerField(primary_key=True, max_length=9)
    email = models.EmailField()
    address = models.ArrayModelField(model_container=Address)
    birthday = models.DateField()
    phone_num = models.BigIntegerField(max_length=15)


class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=30)


class Credit_card(models.Model):
    card_num = models.BigIntegerField(primary_key=True, max_length=16)
    owner_name = models.EmbeddedModelField(model_container=cardOwnerName)
    bank_name = models.CharField(max_length=100)
    ccv = models.IntegerField(primary_key=True, max_length=3)



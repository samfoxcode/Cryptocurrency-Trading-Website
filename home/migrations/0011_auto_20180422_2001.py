# Generated by Django 2.0.1 on 2018-04-22 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20180422_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertransactions',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
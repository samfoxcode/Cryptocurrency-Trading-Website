# Generated by Django 2.0.1 on 2018-04-14 18:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20180414_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweets',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tweets',
            name='ticker',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='tweets',
            unique_together={('ticker', 'timestamp')},
        ),
    ]

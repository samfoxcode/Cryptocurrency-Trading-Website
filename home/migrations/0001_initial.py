# Generated by Django 2.0.1 on 2018-03-09 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10, unique=True)),
                ('website', models.CharField(max_length=30)),
                ('current_price', models.DecimalField(decimal_places=3, max_digits=12)),
                ('gain_loss', models.DecimalField(decimal_places=3, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Old_Prices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('accuracy_projection', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price', models.DecimalField(decimal_places=3, max_digits=12)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Coins')),
            ],
        ),
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('sentiment', models.DecimalField(decimal_places=2, max_digits=12)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Coins')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='old_prices',
            unique_together={('ticker', 'timestamp')},
        ),
    ]

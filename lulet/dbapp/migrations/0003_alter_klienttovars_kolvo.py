# Generated by Django 4.2.10 on 2024-02-18 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbapp', '0002_rename_klientitogo_klienttovars_klient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klienttovars',
            name='kolvo',
            field=models.IntegerField(default=0),
        ),
    ]

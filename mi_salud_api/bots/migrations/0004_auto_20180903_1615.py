# Generated by Django 2.1 on 2018-09-03 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0003_auto_20180828_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmessage',
            name='id_message_response',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bot',
            name='categories',
            field=models.ManyToManyField(related_name='bots', to='bots.Category'),
        ),
    ]

# Generated by Django 2.1 on 2018-08-23 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='v8Ye-819FgLMQaXmkPC_hA', max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('enable', models.BooleanField(default=True)),
            ],
        ),
    ]

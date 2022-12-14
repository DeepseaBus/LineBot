# Generated by Django 3.2.16 on 2022-10-26 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linebotapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(default='', max_length=50)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('job_name', models.CharField(blank=True, max_length=255)),
                ('percentage', models.IntegerField(blank=True)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('mdt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20201215_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='DOB',
            field=models.DateField(blank=True, null=True),
        ),
    ]
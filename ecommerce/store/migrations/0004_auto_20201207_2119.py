# Generated by Django 3.1.3 on 2020-12-07 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_cartdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(max_length=40, null=True)),
                ('cart_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cart_details',
        ),
        migrations.DeleteModel(
            name='cartdetails',
        ),
    ]
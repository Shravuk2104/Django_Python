# Generated by Django 5.1.1 on 2024-10-15 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoreapp', '0004_alter_cart_pid_alter_cart_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoreapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Mobiles'), (2, 'Shoes'), (3, 'Clothes')], verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdetails',
            field=models.CharField(max_length=150, verbose_name='Product Details'),
        ),
    ]
# Generated by Django 5.0.6 on 2024-11-07 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='no-image.jpg', null=True, upload_to=''),
        ),
    ]
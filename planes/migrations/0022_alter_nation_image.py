# Generated by Django 4.0.1 on 2022-02-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0021_nation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='planes/', verbose_name='Изображение'),
        ),
    ]
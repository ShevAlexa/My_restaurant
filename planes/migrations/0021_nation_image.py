# Generated by Django 4.0.1 on 2022-02-22 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0020_airplane_users_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='nation',
            name='image',
            field=models.ImageField(null=True, upload_to='planes/', verbose_name='Изображение'),
        ),
    ]

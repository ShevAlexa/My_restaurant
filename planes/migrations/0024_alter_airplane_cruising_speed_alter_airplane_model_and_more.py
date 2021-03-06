# Generated by Django 4.0.1 on 2022-03-04 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planes', '0023_alter_nation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplane',
            name='cruising_speed',
            field=models.CharField(max_length=5, null=True, verbose_name='Cкорость'),
        ),
        migrations.AlterField(
            model_name='airplane',
            name='model',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-30 10:40

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
                ('url', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('composition', models.CharField(max_length=200, verbose_name='Состав')),
                ('recipe', models.TextField(verbose_name='Рецепт')),
                ('price', models.PositiveIntegerField(default=0, help_text='указать цену в долларах', verbose_name='Цена')),
                ('image', models.ImageField(upload_to='planes/', verbose_name='Изображение')),
                ('cuisine', models.CharField(max_length=50, verbose_name='Кухня')),
                ('url', models.SlugField(max_length=150, unique=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='planes.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='StarRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звёзды рейтинга',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=150, verbose_name='IP-адрес')),
                ('dish', models.ForeignKey(on_delete=django.db.models.fields.CharField, to='planes.dish', verbose_name='Блюдо')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planes.starrating', verbose_name='Звезда')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
    ]

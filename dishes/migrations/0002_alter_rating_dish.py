# Generated by Django 4.0.1 on 2022-01-30 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dishes.dish', verbose_name='Блюдо'),
        ),
    ]

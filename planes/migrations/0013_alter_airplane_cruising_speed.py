# Generated by Django 4.0.1 on 2022-02-21 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0012_remove_airplane_specifications_airplane_constructor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplane',
            name='cruising_speed',
            field=models.CharField(max_length=5, null=True, verbose_name='Крейсерская скорость'),
        ),
    ]

# Generated by Django 4.0.1 on 2022-03-04 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0025_alter_comment_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
    ]
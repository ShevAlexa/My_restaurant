# Generated by Django 4.0.1 on 2022-03-04 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0026_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(null=True, verbose_name='Комментарий'),
        ),
    ]
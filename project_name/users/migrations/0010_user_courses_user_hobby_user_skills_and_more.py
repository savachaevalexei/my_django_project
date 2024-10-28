# Generated by Django 4.2.7 on 2023-12-24 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_work_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='courses',
            field=models.TextField(blank=True, verbose_name='Перечислите курсы, которые проходили'),
        ),
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.CharField(default=1, max_length=255, verbose_name='Перечислите через запятую хобби, которыми увлекаетесь'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='skills',
            field=models.CharField(default=1, max_length=255, verbose_name='Перечислите через запятую навыки, которыми владете'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='work_experience',
            field=models.TextField(blank=True, verbose_name='Опишите опыт работы: где, сколько и кем работали'),
        ),
    ]

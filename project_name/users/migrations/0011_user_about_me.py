# Generated by Django 4.2.7 on 2023-12-24 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_courses_user_hobby_user_skills_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.TextField(blank=True, verbose_name='Расскажите о себе'),
        ),
    ]

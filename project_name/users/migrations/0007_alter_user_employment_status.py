# Generated by Django 4.2.7 on 2023-12-23 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_education_user_employment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employment_status',
            field=models.BooleanField(choices=[(False, 'Ищу работу'), (True, 'Трудоеустроен')], default=0, verbose_name='Трудовой статус'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-23 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_employment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employment_status',
            field=models.CharField(choices=[('Ищу работу', 'Ищу работу'), ('Трудоестроен', 'Трудоеустроен')], max_length=255, verbose_name='Трудовой статус'),
        ),
    ]

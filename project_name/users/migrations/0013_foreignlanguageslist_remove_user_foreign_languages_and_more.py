# Generated by Django 4.2.7 on 2023-12-24 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_foreign_languages_user_publications_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignLanguagesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Иностранные языки',
                'verbose_name_plural': 'Иностранные языки',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='foreign_languages',
        ),
        migrations.AddField(
            model_name='user',
            name='foreign_languages',
            field=models.ManyToManyField(blank=True, related_name='foreign_languages', to='users.foreignlanguageslist', verbose_name='Перечислите через запятую языки, которыми владеете'),
        ),
    ]

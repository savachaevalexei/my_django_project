# Generated by Django 4.2.7 on 2024-01-04 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_remove_comments_parent_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='parrent_id',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-27 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_rename_articlecomments_comments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='comment_id',
            new_name='parent_comment',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='parent_comment_id',
        ),
    ]
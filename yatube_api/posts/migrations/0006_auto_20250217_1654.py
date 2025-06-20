# Generated by Django 3.2.16 on 2025-02-17 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20250217_1252'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_follow',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='user',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_follow'),
        ),
    ]

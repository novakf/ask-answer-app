# Generated by Django 4.2.6 on 2024-01-21 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_answer_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
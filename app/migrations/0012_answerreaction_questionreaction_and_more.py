# Generated by Django 4.2.6 on 2024-01-23 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_reactionanswer_reactionquestion_alter_profile_avatar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_positive', models.BooleanField(default=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_positive', models.BooleanField(default=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.profile')),
            ],
        ),
        migrations.RemoveField(
            model_name='reactionquestion',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='reactionquestion',
            name='user',
        ),
        migrations.DeleteModel(
            name='ReactionAnswer',
        ),
        migrations.DeleteModel(
            name='ReactionQuestion',
        ),
    ]

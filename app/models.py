from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)


class Question(models.Model):
    title = models.CharField(max_length=255, unique=False)
    text = models.TextField(null=True, unique=False)
    rating = models.IntegerField(null=True, default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)


class Answer(models.Model):
    text = models.TextField(null=True)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Profile(models.Model):
    avatar = models.ImageField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

class Reaction(models.Model):
    is_positive = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

TAGS = [
    {
        'id': i,
        'name': f'Tag{i}',
    } for i in range(3)
]

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f"{i}. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        'rating': i,
    } for i in range(15)
]

ANSWERS = [
    {
        'id': i,
        'text': f"{i}. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
        'tag': TAGS[0],
    } for i in range(3)
]

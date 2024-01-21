from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class QuestionManager(models.Manager):
    def getById(self, id):
        question = Question.objects.get(id=id)
        return question

    def tagFilter(self, tag_name):
        tag = Tag.objects.get(name=tag_name)
        return self.filter(tag=tag).order_by('-created_at')

    def newFilter(self):
        questions = self.order_by('-created_at')
        return questions

    def hotFilter(self):
        questions = Question.objects.order_by('-rating')
        return questions

    def answersCount(self):
        count = Answer.objects.filter(Question=self).count()
        return count

    def countQuestions(self):
        return self.count()


class TagManager:
    def mostPopular():
        return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:5]


class ProfileManager:
    def mostPopular():
        return Profile.objects.order_by('-rating')


class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    objects = TagManager()


class Question(models.Model):
    title = models.CharField(max_length=255, unique=False)
    text = models.TextField(null=True, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def countRating(self):
        likes_count = Reaction.objects.filter(
            is_positive=True, question=self).count()
        dislikes_count = Reaction.objects.filter(
            is_positive=False, question=self).count()
        self.rating = likes_count - dislikes_count


class Answer(models.Model):
    text = models.TextField(null=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def countRating(self):
        likes_count = Reaction.objects.filter(
            is_positive=True, answer=self).count()
        dislikes_count = Reaction.objects.filter(
            is_positive=False, answer=self).count()
        self.rating = likes_count - dislikes_count


class Profile(models.Model):
    avatar = models.ImageField(null=True, default='/users/defaultAvatar.jpg')
    rating = models.IntegerField(null=True, default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    objects = ProfileManager()

    def countRating(self):
        answers = Answer.objects.filter(author=self.user).annotate(count=Count('rating'))
        self.rating = answers.count


class Reaction(models.Model):
    is_positive = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)

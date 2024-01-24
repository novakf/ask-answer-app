from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

class ProfileManager:
    def mostPopular():
        return Profile.objects.order_by('-rating')[:5]

class Profile(models.Model):
    avatar = models.ImageField(null=True, default='default-avatar.jpg')
    rating = models.IntegerField(null=True, default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    objects = ProfileManager()

    def countRating(self):
        answers_count = Answer.objects.filter(author=self).count()
        self.rating = answers_count

class QuestionManager(models.Manager):
    def getById(self, id):
        question = Question.objects.annotate(answers_count=Count('answer')).get(id=id)
        return question

    def tagFilter(self, tag_name):
        try:
          tag = Tag.objects.get(name=tag_name)
        except ObjectDoesNotExist:
          return None
        questions = self.filter(tag=tag)
        return questions.order_by('-created_at')
        
    def getAnswers(self, id):
        return Answer.objects.filter(question=id).all()

    def newFilter(self):
        questions = self.annotate(answers_count=Count('answer')).prefetch_related('author', 'tag').order_by('-created_at')
        return questions

    def hotFilter(self):
        questions = Question.objects.annotate(answers_count=Count('answer')).prefetch_related('author', 'tag').order_by('-rating')
        return questions

    def countQuestions(self):
        return self.count()
        
class TagManager:
    def mostPopular():
        return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:7]

class AnswerManager(models.Manager):
    def mostPopular(question):
        return Answer.objects.filter(question=question).order_by('-is_correct', 'created_at')
    def getById(self, id):
        answer = Answer.objects.get(id=id)
        return answer

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    objects = TagManager()

class Question(models.Model):
    title = models.CharField(max_length=255, unique=False)
    text = models.TextField(null=True, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, default=0)

    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def countRating(self):
        likes_count = QuestionReaction.objects.filter(
            is_positive=True, question=self).count()
        dislikes_count = QuestionReaction.objects.filter(
            is_positive=False, question=self).count()
        self.rating = likes_count - dislikes_count


class Answer(models.Model):
    text = models.TextField(null=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    def countRating(self):
        likes_count = AnswerReaction.objects.filter(
            is_positive=True, answer=self).count()
        dislikes_count = AnswerReaction.objects.filter(
            is_positive=False, answer=self).count()
        self.rating = likes_count - dislikes_count

    objects = AnswerManager()

class AnswerReactionManager(models.Manager):
    def toggle_reaction(self, user, answer, reactType):
        if AnswerReaction.objects.filter(user=user, answer=answer).exists():
            reaction = AnswerReaction.objects.get(user=user, answer=answer)
            if reactType == 'like' and reaction.is_positive == False:
              reaction.is_positive = True
              reaction.save()
            elif reactType == 'dislike' and reaction.is_positive == True:
              reaction.is_positive = False
              reaction.save()
            else:
              AnswerReaction.objects.filter(user=user, answer=answer).delete()
        else:
            if reactType == 'like':
              AnswerReaction.objects.create(user=user, answer=answer, is_positive=True)
            else:
              AnswerReaction.objects.create(user=user, answer=answer, is_positive=False)
        answer = Answer.objects.get(id=answer.id)
        answer.countRating()
        answer.save()
        return answer.rating

class AnswerReaction(models.Model):
    is_positive = models.BooleanField(default=True)

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'user'], name='unique_answer_reaction')
        ]

    objects = AnswerReactionManager()

class QuestionReactionManager(models.Manager):
    def toggle_reaction(self, user, question, reactType):
        if QuestionReaction.objects.filter(user=user, question=question).exists():
            reaction = QuestionReaction.objects.get(user=user, question=question)
            if reactType == 'like' and reaction.is_positive == False:
              reaction.is_positive = True
              reaction.save()
            elif reactType == 'dislike' and reaction.is_positive == True:
              reaction.is_positive = False
              reaction.save()
            else:
              QuestionReaction.objects.filter(user=user, question=question).delete()
        else:
            if reactType == 'like':
              QuestionReaction.objects.create(user=user, question=question, is_positive=True)
            else:
              QuestionReaction.objects.create(user=user, question=question, is_positive=False)
        question = Question.objects.get(id=question.id)
        question.countRating()
        question.save()
        return question.rating

class QuestionReaction(models.Model):
    is_positive = models.BooleanField(default=True)

    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'user'], name='unique_question_reaction')
        ]

    objects = QuestionReactionManager()
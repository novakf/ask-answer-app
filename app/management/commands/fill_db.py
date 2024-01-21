from app import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random
from django.utils import timezone


class Command(BaseCommand):
    help = 'This command fills database with random data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int,
                            help='database fill coefficient')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        self.stdout.write("FILL COEF = {ratio}\n")

        fake = Faker()

        users = [User(username=fake.unique.user_name(),
                      password=fake.password(length=5),
                      first_name=fake.first_name(),
                      last_name=fake.last_name(),
                      email=fake.unique.free_email(),
                      last_login=timezone.now()
                      ) for i in range(ratio)]
        User.objects.bulk_create(users)
        self.stdout.write("USERS COMPLETE\n")

        profiles = [models.Profile(user=user) for user in users]
        models.Profile.objects.bulk_create(profiles)
        self.stdout.write("PROFILES COMPLETE\n")

        tags = [models.Tag(name=fake.word()) for i in range(ratio)]
        models.Tag.objects.bulk_create(tags)
        self.stdout.write("TAGS COMPLETE\n")

        questions = []
        for i in range(ratio * 10):
            question = models.Question(title=fake.sentence(), text=fake.text(), author=random.choice(users))
            questions.append(question)
        models.Question.objects.bulk_create(questions)

        for question in questions:
            question.tag.add(random.choice(tags))
        self.stdout.write("QUESTIONS COMPLETE\n")

        answers = []
        for i in range(ratio * 100):
            answer = models.Answer(text=fake.text(), question=random.choice(
                questions), author=random.choice(users), is_correct=random.choice([True, False]))
            answers.append(answer)
        models.Answer.objects.bulk_create(answers)
        self.stdout.write("ANSWERS COMPLETE\n")

        reactions = []
        for i in range(ratio * 200):
            reaction = models.Reaction(user=random.choice(users), is_positive=random.choice([True, False]))
            if random.choice([True, False]):
                reaction.question = random.choice(questions)
            else:
                reaction.answer = random.choice(answers)
            reactions.append(reaction)
        models.Reaction.objects.bulk_create(reactions)

        for index, a in enumerate(models.Answer.objects.all()):
            a.countRating()
            a.save()
        for index, q in enumerate(models.Question.objects.all()):
            q.countRating()
            q.save()

        self.stdout.write("REACTIONS COMPLETE\n")

        for index, q in enumerate(models.Profile.objects.all()):
            q.countRating()
            q.save()

        self.stdout.write("DONE")

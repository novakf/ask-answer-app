from app import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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
        self.stdout.write(f'FILL COEF = {ratio}\n')

        fake = Faker()

        profiles = []
        users=[]
        for i in range(ratio):
            user = get_user_model().objects.create(username=fake.unique.user_name(),
                      first_name=fake.first_name(),
                      last_name=fake.last_name(),
                      email=fake.unique.free_email(),
                      last_login=timezone.now())
            user.set_password('1234')
            user.save()
            users.append(user)
            profile = models.Profile(user=user)
            profiles.append(profile)
            
        models.Profile.objects.bulk_create(profiles)
        self.stdout.write("PROFILES COMPLETE\n")

        tags = []
        for i in range(ratio):
            tag = models.Tag(name=fake.unique.word())
            tags.append(tag)
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

        used_questions = []
        answers = []
        for i in range(ratio * 100):
            curr_question = questions[i % (ratio*10)]
            if curr_question in used_questions:
                correct = False
            else:
                correct = True
                used_questions.append(curr_question)
            
            answer = models.Answer(text=fake.text(), question=curr_question, author=random.choice(users), is_correct=correct)
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

        for i, a in enumerate(models.Answer.objects.all()):
            a.countRating()
            a.save()
        for i, q in enumerate(models.Question.objects.all()):
            q.countRating()
            q.save()

        self.stdout.write("REACTIONS COMPLETE\n")

        for i, p in enumerate(models.Profile.objects.all()):
            p.countRating()
            p.save()

        self.stdout.write("DONE")

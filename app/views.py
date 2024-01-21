from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404
from django.core.paginator import Paginator
from . import models
import re


def index(request):
    filter_param = request.GET.get('tab')
    if filter_param == 'hot':
        questions = models.Question.objects.hotFilter()
    else:
        questions = models.Question.objects.newFilter()
    page_obj = paginate(questions, request)
    tags = models.TagManager.mostPopular()
    best_users = models.Profile.objects.all()
    context = {'questions': page_obj, 'tags': tags, 'best_members': best_users}
    return render(request, 'index.html', context)


def tag(request, tag_name):
    questions = models.Question.objects.tagFilter(tag_name)
    tags = models.TagManager.mostPopular()

    if questions:
        paginator = Paginator(questions, per_page=5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = None

    best_users = models.Profile.objects.all()

    context = {'questions': page_obj,
               'tags': tags,
               'tag': tag_name,
               'best_members': best_users
               }
    return render(request, 'tag.html', context)


def question(request, question_id):
    tags = models.TagManager.mostPopular()
    best_users = models.Profile.objects.all()
    question_id = int(question_id)
    question = models.Question.objects.getById(question_id)
    answers = models.Question.objects.getAnswers(question_id)
    page_obj = paginate(answers, request)
    context = {'question': question,
               'answers': page_obj,
               'tags': tags, 'best_members': best_users}
    return render(request, "question.html", context)


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    if page_number != None and re.search(r'[A-z]', page_number):
        raise Http404
    if int(page_number) < 1:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj

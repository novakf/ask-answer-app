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
    questions = models.QUESTIONS
    tags = TAGS
    if not questions:
        return HttpResponseNotFound('Invalid tag question')
    paginator = Paginator(questions, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'questions': page_obj,
               'tags': tags,
               'tag': tag_name
               }
    return render(request, 'tag.html', context)


def question(request, question_id):
    try:
        question_id = int(question_id)
        if question_id >= len(models.QUESTIONS):
            return HttpResponseNotFound('Invalid question ID')
        context = {'question': models.QUESTIONS[question_id],
                   'answers': models.ANSWERS,
                   'tags': models.TAGS}
        return render(request, "question.html", context)
    except ValueError:
        return HttpResponseNotFound('Invalid question ID')


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
    if page_number != None and (re.search(r'[A-z]', page_number) or int(page_number) > paginator.num_pages or int(page_number) < 1):
        raise Http404
    page_obj = paginator.get_page(page_number)
    return page_obj

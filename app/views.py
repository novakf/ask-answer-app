from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from django.shortcuts import render
from . import models
from .models import TAGS

def index(request):
    questions = models.QUESTIONS
    page_obj = paginate(questions, request)
    tags = TAGS
    context = {'questions': page_obj, 'tags': tags}
    return render(request, 'index.html', context)

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
    if type(page_number) is str:
      return HttpResponseNotFound('Invalid page number')
    page_obj = paginator.get_page(page_number)
    return page_obj

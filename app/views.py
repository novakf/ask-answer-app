from django.shortcuts import redirect, render
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from app import forms
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
    best_users = models.ProfileManager.mostPopular()
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
    best_users = models.ProfileManager.mostPopular()
    context = {'questions': page_obj, 'tags': tags,
               'tag': tag_name, 'best_members': best_users}
    return render(request, 'tag.html', context)


def question(request, question_id):
    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    question_id = int(question_id)
    question = models.Question.objects.getById(question_id)
    answers = models.Question.objects.getAnswers(question_id)
    page_obj = paginate(answers, request)
    context = {'question': question, 'answers': page_obj,
               'tags': tags, 'best_members': best_users}
    return render(request, "question.html", context)

def log_out(request):
    logout(request)
    return redirect(reverse('login'))

def signup(request):
    return render(request, 'signup.html')


@csrf_protect
def log_in(request):
    if request.method == "GET":
      login_form = forms.LoginForm(request.GET)
    if request.method == "POST":
      login_form = forms.LoginForm(request.POST)
      if login_form.is_valid():
          user = authenticate(request=request, **login_form.cleaned_data)
          if user is not None:
              login(request, user)
              if (request.POST.get('continue')):
                  return redirect(request.POST.get('continue'))
              else:
                  return redirect('index')
          login_form.add_error(None, "Wrong password or user does not exist")

    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    context = {'tags': tags, 'best_members': best_users, 'form': login_form}
    return render(request, 'login.html', context=context)


def settings(request):
    return render(request, 'settings.html')


@login_required(login_url='/login', redirect_field_name='continue')
def ask(request):
    return render(request, 'ask.html')


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    if page_number != None and re.search(r'[A-z]', page_number):
        raise Http404
    if page_number != None and int(page_number) < 1:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj

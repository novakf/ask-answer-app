from django.shortcuts import redirect, render
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from app import forms
from django.contrib.auth.models import User
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
    print(request.user)
    context = {'questions': page_obj, 'tags': tags, 'best_members': best_users, 'current_user': request.user}
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
               'tag': tag_name, 'best_members': best_users, 'current_user': request.user}
    return render(request, 'tag.html', context)

def question(request, question_id):
    if request.method == 'GET':
        answer_form = forms.AnswerForm()
    else:
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.save(request, question_id)
            answers = models.AnswerManager.mostPopular(question_id)
            page_obj = paginate(answers, request)
            return redirect(f'/question/{question_id}/?page={page_obj.paginator.num_pages}')
        else:
            answer_form.add_error("Invalid arguments")
    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    question_id = int(question_id)
    question = models.Question.objects.getById(question_id)
    answers = models.AnswerManager.mostPopular(question_id)
    page_obj = paginate(answers, request)
    context = {'question': question, 'answers': page_obj,
               'tags': tags, 'best_members': best_users, 'current_user': request.user, 'form': answer_form}
    return render(request, "question.html", context)

@login_required
def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def sign_up(request):
    if request.method == "GET":
      signup_form = forms.RegistrationForm()
    if request.method == "POST":
      signup_form = forms.RegistrationForm(request.POST)
      if signup_form.is_valid():
          user = signup_form.save()
          if user is not None:
              login(request, user)
              return redirect('index')
          
          signup_form.add_error(None, "User saving error")

    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    context = {'tags': tags, 'best_members': best_users, 'form': signup_form, 'current_user': request.user}
    return render(request, 'signup.html', context=context)


@csrf_protect
def log_in(request):
    if request.method == "GET":
      login_form = forms.LoginForm()
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
    context = {'tags': tags, 'best_members': best_users, 'form': login_form, 'current_user': request.user}
    return render(request, 'login.html', context=context)

@login_required(login_url='/login', redirect_field_name='continue')
def settings(request):
    user = models.User.objects.get(username=request.user.username)
    data = {'username': user.username, "email": user.email}
    if request.method == "GET":
      settings_form = forms.ProfileEditForm(initial=data)
    if request.method == "POST":
      settings_form = forms.ProfileEditForm(request.POST)
      if settings_form.is_valid():
            user = settings_form.save(request)
            print(user)
            return redirect(reverse('settings'))
            
    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    context = {'tags': tags, 'best_members': best_users, 'form': settings_form, 'current_user': request.user}
    return render(request, 'settings.html', context=context)


@login_required(login_url='/login', redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        question_form = forms.QuestionForm()
    if request.method == 'POST':
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(request.user)
            return redirect('question', question.id)
    tags = models.TagManager.mostPopular()
    best_users = models.ProfileManager.mostPopular()
    context = {'tags': tags, 'best_members': best_users, 'form': question_form, 'current_user': request.user}
    return render(request, "ask.html", context)


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    if page_number != None and re.search(r'[A-z]', page_number):
        raise Http404
    if page_number != None and int(page_number) < 1:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj

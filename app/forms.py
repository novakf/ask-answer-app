from django import forms
from app import models
from django.contrib.auth import authenticate
from django.contrib import messages

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput) 
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput) 

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password']

    def clean(self):
        try:
          password = self.cleaned_data['password']
          password_check = self.cleaned_data['password_check']

          if password != password_check:
              raise forms.ValidationError('Passwords do not match')
        except KeyError:
            return
        
    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        user = models.User.objects.create_user(**self.cleaned_data)
        models.Profile.objects.create(user=user, avatar='default-avatar.jpg')
        return user
    
class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False

    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    
    class Meta:
        model = models.User
        fields = ['username', 'email', 'avatar']

    def clean(self):
        username = self.cleaned_data.get('username')
        if models.User.objects.filter(username=username).count() > 1:
            raise forms.ValidationError("This username already in use.")
        return

    def save(self, request):
        user = models.User.objects.get(username=request.user)
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        profile = models.Profile.objects.get(user=user.id)
        
        if self.cleaned_data.get('avatar'):
            print(self.cleaned_data.get('avatar'))
            profile.avatar = self.cleaned_data.get('avatar')

        if username:
            user.username = username

        if email:
            user.email = email

        user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully!')

class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    text = forms.CharField(max_length=500, widget=forms.Textarea)
    tags = forms.CharField(required=False)
    
    def save(self, user):
        super().clean()
        profile = models.Profile.objects.get(user=user)
        tags_names = []
        if self.cleaned_data['tags']:
            tags_names.extend(self.cleaned_data['tags'].split(','))

        tags = []
        for tag_name in tags_names:
            if models.Tag.objects.filter(name=tag_name).exists():
                tags.append(models.Tag.objects.get(name=tag_name))
            else:
                new_tag = models.Tag(name=tag_name)
                new_tag.save()
                tags.append(new_tag)

        new_question = models.Question.objects.create(author=profile,
                                        title=self.cleaned_data['title'],
                                        text=self.cleaned_data['text'])
        new_question.tag.set(tags)
        return new_question

    class Meta:
        model = models.Question
        fields = ['title', 'text', 'tags']

class AnswerForm(forms.Form):
    answer = forms.CharField(required=True, max_length=500,
                             widget=forms.Textarea(attrs={'placeholder': 'Enter an answer...'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = ''

    def save(self, request, question_id):
        user = models.Profile.objects.get(user=request.user)

        question = models.Question.objects.get(id=question_id)
        answer = self.cleaned_data['answer']
      
        answer_obj = models.Answer.objects.create(text=answer, question=question, author=user)
        messages.success(request, 'Thanks for your answer!')
        return answer_obj
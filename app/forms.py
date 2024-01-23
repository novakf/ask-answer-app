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
        return models.User.objects.create_user(**self.cleaned_data)
    
class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False

    avatar = forms.ImageField(required=False, widget=forms.FileInput)
    
    class Meta:
        model = models.User
        fields = ['username', 'email', 'avatar']

    def clean(self):
        return

    def save(self, request):
        user = models.User.objects.get(username=request.user)
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username:
            user.username = username

        if email:
            user.email = email

        user.save()
        messages.success(request, 'Profile updated successfully!')

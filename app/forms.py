from django import forms
from app import models
from django.contrib.auth import authenticate

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
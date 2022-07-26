from django import forms 
from .models import Profile
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields=['date_of_birth','photo']


class LoginForm(forms.Form):
    username=forms.CharField()  
    password=forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput,label="Password")
    password2=forms.CharField(widget=forms.PasswordInput,label="Repet Password")

    class Meta:
        model=User
        fields=['username','first_name','email']
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError("Passwords do not match")
        return cd['password2']
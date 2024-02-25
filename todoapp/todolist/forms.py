from django import forms
from django.contrib.auth.models import User

from .models import Task, Profile

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'finished', 'signif']
        widgets = {
            'finish_date':forms.DateTimeInput()
        }

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'signif']
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    rep_password = forms.CharField(label='Repeate password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_rep_password(self):
        cd = self.cleaned_data
        if len(cd['password']) < 6:
            raise forms.ValidationError("Too short password.\n It's should be at least 6 characters.")
        if cd['password'] != cd['rep_password']:
            raise forms.ValidationError("Passwords don't match")
        return cd['rep_password']
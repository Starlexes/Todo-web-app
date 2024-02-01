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

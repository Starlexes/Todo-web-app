from django import forms
from todolist.models import Task

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'finished', 'signif']

class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'signif']


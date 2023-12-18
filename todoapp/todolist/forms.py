from django.forms import ModelForm
from todolist.models import Task

class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'finished', 'signif']

class AddTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'finish_date', 'signif']


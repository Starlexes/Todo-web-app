from django.contrib import admin
from django.urls import path, include
from django.views.generic import ListView

from . import views 
from .utils import *

app_name = 'todolist'

urlpatterns = [
        path('', views.main_page, name='home'),
        path('about/<int:task_id>', views.about, name='task_detail'),
        path('edit/<int:task_id>', views.edit_task, name='edit_task'),
        path('delete/<int:task_id>', views.delete_task, name='delete_task'),
        path('add-task', views.add_task, name='add_task')

]






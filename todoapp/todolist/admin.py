from django.contrib import admin
from todolist.models import Task, Importance
# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'finish_date', 'finished','signif']

    search_fields = ['title']
    ordering = ['title', '-finish_date','finished']

@admin.register(Importance)
class Importance(admin.ModelAdmin):
    list_display = ['importance']
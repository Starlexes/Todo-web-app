from django.contrib import admin
from todolist.models import Task, Importance, Profile
# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'finish_date', 'finished','signif']

    search_fields = ['title']
    ordering = ['title', '-finish_date','finished']

@admin.register(Importance)
class ImportanceAdmin(admin.ModelAdmin):
    list_display = ['importance']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tasks','date_of_birth', 'photo']
    raw_id_fields = ['user']

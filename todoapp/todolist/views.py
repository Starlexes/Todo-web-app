import json
import csv
from datetime import datetime
from django.http import HttpResponse
from django.core.serializers import serialize
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response

from .models import Task, Importance, Profile
from .forms import EditTaskForm, AddTaskForm, UserEditForm, \
                    ProfileEditForm, UserRegistrationForm, SearchForm

from .serializers import TaskSerializer

# Create your views here.
importances = ['Low', 'Medium', 'High', 'Critical']


def get_user(request):
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    return user

@login_required(login_url='login/')
def main_page(request, tag_slug=None):
   
    title = 'Todo'
    user = get_user(request)
    
    tag = None
    tasks = Task.objects.filter(user=user)
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            return redirect('search')
        
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        tasks= Task.objects.filter(tag__in = [tag])
    paginator = Paginator(tasks, 6)
    page_number = request.GET.get('page', 1)
    try:
        tasks = paginator.page(page_number)

    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        tasks = paginator.page(1)

    return render(request, 'todolist/index.html', {"title" : title, "tasks" : tasks, "tag":tag} )

def about(request, task_id):
    title = 'About task'

    task = get_object_or_404(Task, id=task_id)

    return render(request, 'todolist/detail.html', {'task':task,
                                                    'title':title})

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    sent = False
    
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            cd = form.cleaned_data
            slug = slugify(cd['title'])
            task.title = cd['title']
            task.slug = slug
            task.description = cd['description']
            task.finish_date = cd['finish_date']
            task.finished = cd['finished']
            task.signif = Importance.objects.get(pk=request.POST['signif'])
            task.save()
            sent = True
        return redirect(task, task_id=task.id)
    else:
        form = EditTaskForm(instance=task)

    return render(request, 'todolist/edit_task.html', {
        'sent':sent,
        'form':form,
        'task': task,
        'importances':importances
    })

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.del_task()
       
        return redirect('todolist:home')
    return render(request, 'todolist/delete_task.html')
    
def add_task(request):
    sent = False
    user = get_user(request)
    print(request.user.id)
    if user is not None:  # Проверка наличия пользователя
        if request.method == 'POST':
            form = AddTaskForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                slug = slugify(cd['title'])
                title = request.POST['title']
                description = request.POST['description']
                finish_date = request.POST['finish_date']
                finished = False
                signif = Importance.objects.get(pk=request.POST['signif'])
                
                task = Task(title=title, slug=slug, description=description, finish_date=finish_date,
                            finished=finished, signif=signif, user=user)
                task.save()
                sent = True
                return render(request, 'todolist/new_task.html', {'form':form, 'task':task, 'sent':sent})
        
        else:
            form = AddTaskForm()
        return render(request, 'todolist/new_task.html', {'form': form, 'sent': sent})
    else:
       
        return HttpResponse("User not found.")
    
@login_required(login_url='login/')
def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('todolist:home')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'todolist/edit_profile.html', { 'user_form':user_form,
                                                                'profile_form':profile_form})

@login_required(login_url='login/')                                                                
def profile(request):
    user_id = request.user.id
    complete_tasks = Task.objects.filter(finished=True)
    uncomlete_tasks = Task.objects.filter(finished=False)
    profile_data = Profile.objects.get(pk=user_id)
    return render(request, 'todolist/profile.html', {
        'ctasks':complete_tasks,
        'unctasks':uncomlete_tasks,
        'profile_data': profile_data,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'todolist/register_done.html', {'new_user': new_user})

    else:
        form = UserRegistrationForm()
    return render(request, 'todolist/register.html', {
        'user_form':form,
    })

def export_tasks(request, task_id=None):
    user = get_user(request)
    
    if task_id is None:
        file_name = f'tasks of {user.username}.json'
        data = Task.objects.filter(user=user)
    else:
        data = Task.objects.filter(user=user, pk=task_id)
        file_name = f'task{task_id} of {user.username}.json'

    serialized_data = serialize('json', data) 
    data_list = json.loads(serialized_data)

    for item in data_list:
                
        fd = datetime.fromisoformat(item['fields']['finish_date'].replace('Z', '+00:00')) 
        item['fields']['finish_date'] = fd.strftime('%Y-%m-%d %H:%M:%S')

    response = HttpResponse(content_type='application/json') 
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    json.dump(data_list, response, ensure_ascii=False)
    return response

def export_to_csv(request, task_id = None):
    user = get_user(request)
    
    if task_id is None:
        file_name = f'tasks of {user.username}.csv'
        data = Task.objects.filter(user=user).only('title', 'description', 'finish_date', 'finished', 'signif')
    else:
        data = Task.objects.filter(user=user, pk=task_id).only('title', 'description', 'finish_date', 'finished', 'signif')
        file_name = f'task{task_id} of {user.username}.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Finish_date', 'Finished', 'Signif'])
    for d in data:
        writer.writerow([d.title, d.description, d.finish_date, d.finished, d.signif])

    return response

def task_search(request):
   
    user = get_user(request)
    query = request.GET.get('query')
    result = []

    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Task.objects.annotate(search=SearchVector('title', 'description', 'tag')
                                            ).filter(user=user, search=query)
    return render(request, 'todolist/search.html', {'srch_form':form,                                             
                                                   'query':query,
                                                   'results':results})

# Viewsets

class TaskViewSet( viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('title')
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]

class ImportantTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    signif = Importance.objects.filter(Q(importance='High') | Q(importance='Critical'))
    queryset = Task.objects.filter(signif__in=signif)
    permission_classes = [permissions.IsAuthenticated,permissions.IsAdminUser]

class TaskAboutViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        task_slug = self.kwargs.get('slug')
        queryset = self.queryset.filter(slug=task_slug)
        return queryset
            
        


        

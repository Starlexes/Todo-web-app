from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from rest_framework import permissions, viewsets

from .models import Task, Importance, Profile
from .forms import EditTaskForm, AddTaskForm, UserEditForm, ProfileEditForm
from .serializers import TaskSerializer

# Create your views here.
importances = ['Low', 'Medium', 'High', 'Critical']


@login_required(login_url='login/')
def main_page(request, tag_slug=None):
   
    title = 'Todo'
    
    tag = None
    tasks = Task.objects.all()
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
            task = Task(title=title, slug=slug,description=description, finish_date=finish_date,
                        finished=finished, signif=signif )
            task.save()
            sent = True
        return render(request, 'todolist/new_task.html', {'form':form,
                                                    'task':task,
                                                    'sent':sent})
    
    else:
        form = AddTaskForm()
    return render(request, 'todolist/new_task.html', {'form':form,
                                                      'sent':sent})
    
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

# Viewsets

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all().order_by('title')
    permission_classes = [permissions.IsAdminUser]

class ImportantTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    signif = Importance.objects.filter(Q(importance='High') | Q(importance='Critical'))
    queryset = Task.objects.filter(signif__in=signif)
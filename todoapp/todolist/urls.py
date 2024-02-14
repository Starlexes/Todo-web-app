from django.contrib import admin
from django.urls import path, include
from django.views.generic import ListView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from . import views 
from .utils import *

app_name = 'todolist'

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='tasks')
router.register(r'important', views.ImportantTaskViewSet)


urlpatterns = [
        path('', views.main_page, name='home'),
        path('tag/<slug:tag_slug>', views.main_page ,name='home_by_tags'),
        path('about/<int:task_id>', views.about, name='task_detail'),
        path('edit/<int:task_id>', views.edit_task, name='edit_task'),
        path('delete/<int:task_id>', views.delete_task, name='delete_task'),
        path('add-task', views.add_task, name='add_task'),
        path('login/', auth_views.LoginView.as_view(), name = 'login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('todolist:password_change_done')), name='password_change'),
        path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = "registration/password_change_done.html" ), name='password_change_done'),
        path('edit-profile/', views.edit_profile, name='edit_profile'),
        path('profile/', views.profile, name='profile'),
        path('api/about/<int:pk>/', views.TaskAboutViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='api-task-about'),
        path('api/', include(router.urls))
]       

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)




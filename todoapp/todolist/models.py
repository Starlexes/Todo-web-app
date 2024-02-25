from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', verbose_name='User')
    title = models.CharField(max_length=50, verbose_name='Title')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(verbose_name='Description')
    finish_date = models.DateTimeField(verbose_name='Date')
    finished = models.BooleanField(default=False, verbose_name='Finished')
    signif = models.ForeignKey('Importance', on_delete=models.PROTECT, null=True,
                               verbose_name='Importance')
    tag = TaggableManager()

    def __str__(self):
        return self.title
    
    def del_task(self):
        self.delete()
    
    class Meta:
        ordering = [ 'signif','finished', 'title', '-finish_date']

    def get_absolute_url(self):
        return reverse('todolist:task_detail' , args=[self.id])

class Importance(models.Model):
    class ImportantTypes(models.TextChoices):
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'
        CRITICAL = 'Critical'

    sygnif = models.CharField(max_length=100, db_index=True, verbose_name='Importance')
    importance = models.CharField(max_length=20, choices=ImportantTypes.choices, default=ImportantTypes.LOW)

    def __str__(self):
        return self.importance

    def get_absolute_url(self):
        return reverse()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='%Y/%m/%d/', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


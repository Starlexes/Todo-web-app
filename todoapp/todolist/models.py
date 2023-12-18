from django.db import models
from django.urls import reverse
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(verbose_name='Description')
    finish_date = models.DateTimeField(verbose_name='Date')
    finished = models.BooleanField(default=False, verbose_name='Finished')
    signif = models.ForeignKey('Importance', on_delete=models.PROTECT, null=True,
                               verbose_name='Importance')

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





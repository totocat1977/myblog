import datetime

from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import AbstractUser

# from time import gmtime, strftime

'''
# Create your models here.
class myuser(AbstractUser):
    dept = models.CharField(max_length=100, default='IT')
    desc = models.CharField(max_length=100)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dept = models.CharField(max_length=100)
    def __str__(self):
        return self.dept
'''        
    
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
        

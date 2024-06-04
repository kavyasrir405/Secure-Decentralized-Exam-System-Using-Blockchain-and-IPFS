
import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    user_id = models.CharField(max_length=9, unique=True, primary_key=True)  # Length of 'user' + 4 digits

    def __str__(self):
         return f"{self.username} ({self.user_type}) - {self.user_id}"

    def save(self, *args, **kwargs):
        if not self.user_id:  
            self.user_id = 'user' + ''.join(random.choices(string.digits, k=4))
        super().save(*args, **kwargs)

class Quiz(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    quiz_name = models.CharField(max_length=200)
    quiz_id = models.CharField(max_length=9, unique=True, primary_key=True)  
    def __str__(self):
        return  f"{self.quiz_name} - {self.quiz_id}"

    def save(self, *args, **kwargs):
        if not self.quiz_id: 
            self.quiz_id = 'quiz' + ''.join(random.choices(string.digits, k=4))
        super().save(*args, **kwargs)

class Question(models.Model):
    question_id = models.CharField(max_length=9, unique=True, primary_key=True)  
    question_text = models.CharField(max_length=1000)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  
    question_marks = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.question_text} - {self.quiz}"

    def save(self, *args, **kwargs):
        if not self.question_id: 
            self.question_id = f"{self.quiz.quiz_id}" + '-'.join(random.choices(string.digits, k=4))
        super().save(*args, **kwargs)

class Answer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks=models.IntegerField(default=0)
    answer_pic = models.ImageField(upload_to='answers')

class quiz_attempted(models.Model):
    quiz_attempt =  models.ForeignKey(Quiz, on_delete=models.CASCADE) 
    user_attempt= models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class evaluated(models.Model):
    quiz_eval=models.ForeignKey(Quiz, on_delete=models.CASCADE) 
    user_eval=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  


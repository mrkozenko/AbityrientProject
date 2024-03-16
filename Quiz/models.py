from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import request
from django.utils import timezone

from TGBot.models import TGUser


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    is_show = models.BooleanField(default=True, verbose_name="Відображати")
    created = models.DateField(default=timezone.now, auto_created=True, verbose_name="Час створення")

    def __str__(self):
        return f"{self.title}|{self.created}"

    def get_questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name = "вікторину"
        verbose_name_plural = "вікторини"


class Question(models.Model):
    question_text = models.CharField(max_length=500, verbose_name="Питання")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score_value = models.IntegerField(default=1, verbose_name="Кількість балів")

    def __str__(self):
        return self.question_text

    def get_answers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name = "питання"
        verbose_name_plural = "питання"


class Answer(models.Model):
    answer_text = models.CharField(max_length=500, verbose_name="Варіант відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Правильна відповідь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = "відповідь"
        verbose_name_plural = "відповіді"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Вікторина")
    user = models.ForeignKey(TGUser, on_delete=models.CASCADE,default=0, verbose_name="Абітурієнт")
    score = models.IntegerField( verbose_name="Кількість балів")
    completed = models.DateTimeField(default=timezone.now, auto_created=True,verbose_name="Час завершення")

    def __str__(self):
        return f"{self.quiz.title}|{self.user_id}"

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результати"
        unique_together = (("user", "quiz"),)
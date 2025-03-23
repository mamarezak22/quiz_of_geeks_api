from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
# Create your models here.
class Question(models.Model):
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answers')
    is_correct = models.BooleanField(default=False)


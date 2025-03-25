from django.db import models
from django.contrib.auth import get_user_model

from questions.models import Category
from .categories import  game_status

User = get_user_model()
# Create your models here.


class GameSession(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='games_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="games_as_user2")
    status = models.CharField(max_length=1,choices = game_status,default="p")
    current_round = models.PositiveSmallIntegerField(default=1)
    user1_point = models.PositiveSmallIntegerField(default = 0)
    user2_point = models.PositiveSmallIntegerField(default = 0)
    #the categories that been asked by users to select.
    selected_categories = models.ManyToManyField(Category,blank=True,related_name='selected_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)




    def __str__(self):
        return f"{self.user1} vs {self.user2}"

class GameRound(models.Model):
    game = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True)
    round_number = models.PositiveSmallIntegerField(default = 0)
    selected_question_category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True)
    user1_answered_questions = models.PositiveSmallIntegerField(default = 0)
    user2_answered_questions = models.PositiveSmallIntegerField(default = 0)

class GameQuestion(models.Model):
    question = models.ForeignKey("questions.Question", on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey(GameRound, on_delete=models.SET_NULL, null=True,related_name="questions")
    question_number = models.PositiveSmallIntegerField(default = 0)
    user1_seen_time = models.DateTimeField(null=True)
    user2_seen_time = models.DateTimeField(null=True)





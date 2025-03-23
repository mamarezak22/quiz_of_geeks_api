from django.db import models
from django.contrib.auth import get_user_model
from .categories import  game_status

User = get_user_model()
# Create your models here.

class GameSession(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='games_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="games_as_user2")
    status = models.CharField(max_length=1,choices = game_status)
    user1_point = models.PositiveSmallIntegerField(default = 0)
    user2_point = models.PositiveSmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)


    def __str__(self):
        return f"{self.user1} vs {self.user2}"

class GameRound(models.Model):
    game = models.ForeignKey(GameSession, on_delete=models.SET_NULL, null=True)
    round_number = models.PositiveSmallIntegerField(default = 0)
    selected_question_category = models.ForeignKey("questions.Category", on_delete=models.PROTECT, null=True)
    done_by_user1 = models.BooleanField(default=False)
    done_by_user2 = models.BooleanField(default=False)

class GameQuestion(models.Model):
    question = models.ForeignKey("questions.Question", on_delete=models.SET_NULL, null=True)
    round = models.ForeignKey(GameRound, on_delete=models.SET_NULL, null=True,related_name="questions")
    question_number = models.PositiveSmallIntegerField(default = 0)
    user1_seen_time = models.DateTimeField(null=True)
    user2_seen_time = models.DateTimeField(null=True)





from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserGeneralStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    coin = models.PositiveIntegerField(default=100)
    count_of_won_games = models.PositiveSmallIntegerField(default=0)
    count_of_loss_games = models.PositiveSmallIntegerField(default=0)
    count_of_tie_games = models.PositiveSmallIntegerField(default=0)

class UserQuestionCategoryStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey("questions.Category",on_delete=models.PROTECT)
    count_of_correct_answers = models.PositiveIntegerField(default=0)
    count_of_wrong_answers = models.PositiveIntegerField(default=0)


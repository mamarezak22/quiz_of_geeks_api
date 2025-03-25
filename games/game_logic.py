from typing import Tuple
from django.contrib.auth.models import AbstractBaseUser
from django.db import Q, transaction

from models import GameSession

def user_has_open_games_more_than_limit(user:AbstractBaseUser)->bool:
    count_of_open_games_by_user = GameSession.objects.filter(Q(user1 = user) | Q(user2 = user)).count()
    return count_of_open_games_by_user == 5

def find_available_game(user:AbstractBaseUser)->GameSession|None:
    with transaction.atomic():
        opened_games = GameSession.objects.select_for_update().filter(status="p")
        for opened_game in opened_games:
            if opened_game.user1 == user:
                continue
            else:
                available_game = opened_game
                available_game.usr2 = user
                available_game.status = "s"
                available_game.save()
                return available_game

def create_game(user:AbstractBaseUser)->GameSession:
    game = GameSession.objects.create(user1 = user)
    return game

def handle_start_game(user:AbstractBaseUser)->Tuple[GameSession|None,str,int]:
    if user_has_open_games_more_than_limit(user):
        return None,"already_have_5_games",400

    if available_game := find_available_game(user):
        return available_game,"joined to game",200

    game = create_game(user)
    return game,"new game created",200

def is_user_turn_to_select_category(user : AbstractBaseUser,game:GameSession)->bool:
    game_round = game.current_round
    is_user1 = game.user1 == user

    if is_user1:
        if game_round %2==0:
            return False
        return True

    if not is_user1:
        if game_round %2==1:
            return True
        return False



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from django.db.models import Q

from questions.models import Question
from .game_logic import handle_start_game,is_user_turn_to_select_category
from utils.maps import status_codes
from .models import GameSession, GameRound
from .serializers import GameSerializer
from .permissions import AccessToGamePermission
from questions.categories import question_categories

#game/start
class StartGameView(APIView):
    def post(self, request):
        user = request.user
        game , resp_text , status_code = handle_start_game(user)
        if game:
            game_URI:str = reverse("game-detail",kwargs={"pk":game.pk})
        status_code = status_codes[status_code]
        if game:
            return Response({"detail" : resp_text},status = status_code,headers = {"location":game_URI})
        return Response({"detail" : resp_text},status = status_code)

#game/{game_id}
class GameDetailView(APIView):
    permission_classes = [AccessToGamePermission]
    def get(self,request,game_id):
            try:
                game = GameSession.objects.get(pk=game_id)
            except GameSession.DoesNotExist:
                return Response({"detail": "game with this id does not exist"}, status=status_codes[404])
            self.check_object_permissions(request,game)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status_codes[200])


#game/{game_id}/select
class SelectCategoryView(APIView):
    permissions_classes = [AccessToGamePermission]
    def post(self, request,game_id,selected_category):
        user = request.user
        try :
            game = GameSession.objects.get(pk=game_id)
        except GameSession.DoesNotExist:
            return Response({"detail" : "game with this id does not exist"},status = status_codes[404])
        if user not in (game.user1 and game.user2):
            return Response({"detail" : "dont have acsess to this game"},status = status_codes[403])
        self.check_object_permissions(request,game)

        if is_user_turn_to_select_category(user,game) is None:
            return Response({"detail":"there is not your time to select category"})
        current_round = game.current_round
        if current_round.user1_answered_questions != 3 and current_round.user2_answered_questions != 3:
            return Response({"detail":"last round still unfinished"},status = status_codes[400])
        new_round = GameRound.objects.create(game=game,round_number = game.current_round+1)
        game.current_round+=1
        game.save()
        selected_categories = [category.name for category in game.selected_categories]
        # TODO : return 2 category for this round.(it must not have
        return Response({"detail" : "category selected."},status = status_codes[200])


#game/{game_id}/answer
class QuestionDetailView(APIView):
    permissions_classes = [AccessToGamePermission]
    def post(self,request,game_id):
        user = request.user
        try:
            game = GameSession.objects.get(pk=game_id)
        except GameSession.DoesNotExist:
            return Response({"detail" : "game with this id does not exist"},status = status_codes[404])
        if user not in (game.user1 and game.user2):
            return Response({"detail" : "dont have acsess to this game"},status = status_codes[403])
        self.check_object_permissions(request,game)
        current_round = game.current_round
        is_user_1 = user == game.user1
        if is_user_1:
            answered_questions = current_round.user1_answered_questions
        if not is_user_1:
            answered_questions = current_round.user2_answered_questions

        if answered_questions >=3:
            return Response({"detail" : "already answered your questions"},status = status_codes[400])

        selected_question = Question.objects.get(category__name=current_round.selected_question_category)



class UserGameListView(APIView):
    permissions_classes = [IsAuthenticated]
    def get(self,request,game_id):
        user = request.user
        user_games = GameSession.objects.filter(Q(user1=user) | Q(user2=user))
        serializer = GameSerializer(user_games, many=True)
        return Response(serializer,status=status_codes[200])








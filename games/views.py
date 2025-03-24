from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse

from .game_logic import handle_start_game,is_user_turn_to_select_category
from utils.maps import status_codes
from .models import GameSession, GameRound
from .serializers import GameSerializer
from .permissions import AccessToGamePermission

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


#game/{game_id}/select/{category_name}
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
        game.current_round+=1
        game.save()
        current_round = GameRound.objects.get(game=game_id,round_number=game.current_round)
        current_round.selected_category = selected_category
        current_round.save()
        return Response({"detail" : "category selected."},status = status_codes[200])





# TODO : list_user_games








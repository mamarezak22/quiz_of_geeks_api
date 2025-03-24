from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse

from .game_logic import handle_start_game
from utils.maps import status_codes
from .models import GameSession
from .serializers import GameSerializer


class StartGameView(APIView):
    permissions_classes = IsAuthenticated
    #game/start
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
    def get(self, request,game_id):
        try :
            game = GameSession.objects.get(pk=game_id)
        except GameSession.DoesNotExist:
            return Response({"detail" : "game with this id does not exist"},status = status_codes[404])
        serializer = GameSerializer(game)
        return Response(serializer.data,status = status_codes[200])








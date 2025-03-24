from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse

from .game_logic import handle_start_game
from utils.maps import status_codes


#/game/start
class StartGameView(APIView):
    permissions_classes = IsAuthenticated
    def post(self, request):
        user = request.user
        game , resp_text , status_code = handle_start_game(user)
        if game:
            game_URI:str = reverse("game-detail",kwargs={"pk":game.pk})
        status_code = status_codes.get(status_code)
        return Response({"detail" : resp_text},status = status_code,headers = {"location":game_URI})








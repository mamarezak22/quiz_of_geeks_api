from rest_framework.serializers import ModelSerializer
from .models import GameSession

class GameSerializer(ModelSerializer):
    class Meta:
        model = GameSession
        fields = '__all__'

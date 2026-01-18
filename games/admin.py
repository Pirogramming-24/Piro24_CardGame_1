# games/admin.py
from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # 관리자 목록 화면에서 보여줄 필드들
    list_display = ('id', 'Attacker', 'AttackerCard', 'Defender', 'DefenderCard','isBiggerScoreWin','Winner','isGameOngoing')
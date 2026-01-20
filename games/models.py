from django.db import models
from django.conf import settings

class Game(models.Model):
    # 1. 공격자 (Attacker)
    Attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='attack_games'
    )
    AttackerCard = models.IntegerField()

    # 2. 방어자 (Defender)
    Defender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='defend_games'
    )
    # 처음엔 카드를 안 냈으니 비어있어야 함 (null=True)
    DefenderCard = models.IntegerField(null=True, blank=True) 

    # 3. 승리 규칙
    # True: 더 큰 점수가 이김 / False: 더 작은 점수가 이김
    isBiggerScoreWin = models.BooleanField(default=True) 
    
    # 4. 승리자
    # 비길 수도 있고, 진행 중일 땐 없으므로 비어있어야 함 (null=True)
    Winner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='won_games'
    )

    # 5. 게임 진행 여부
    # True: 진행 중 / False: 종료
    isGameOngoing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.Attacker} vs {self.Defender}"
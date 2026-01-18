from django.db import models

# Create your models here.

def Game():
    Attacker = models.ForeignKey(

    )
    AttackerCard = models.IntegerField()
    Defender = models.ForeignKey(

    )
    DefenderCard = models.IntegerField()
    isBiggerScoreWin = models.BooleanField() #더 큰 점수가 이기는 게임이면 True,작은 점수가 이기면 False
    Winner = models.ForeignKey(
        
    )
    isGameOngoing = models.BooleanField(default=True)
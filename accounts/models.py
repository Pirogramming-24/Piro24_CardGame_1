from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, verbose_name="닉네임")
    score = models.IntegerField(default=0, verbose_name="점수")

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname=f"User_{self.username}"
        super().save(*args, **kwargs)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 기존 UserAdmin의 설정(fieldsets) 뒤에다가 '추가 정보' 섹션을 붙이는 코드입니다.
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {'fields': ('nickname', 'score')}),
    )
    
    # 리스트 화면(목록)에서도 점수가 보이게 설정
    list_display = ('username', 'nickname', 'score', 'is_active', 'is_staff')
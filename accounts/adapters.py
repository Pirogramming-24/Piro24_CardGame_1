# accounts/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        # 기본적으로 유저 정보를 채워넣는 기능 호출
        user = super().populate_user(request, sociallogin, data)
        
        # 소셜에서 넘어온 이메일 확인 (예: sihyun8870@naver.com)
        email = user.email
        
        if email:
            # '@'를 기준으로 앞부분만 잘라내기 (결과: sihyun8870)
            username_from_email = email.split('@')[0]
            user.username = username_from_email
            
        return user
import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

# 상단에서 로드
load_dotenv()

class Command(BaseCommand):
    help = '환경변수를 바탕으로 소셜 어플리케이션 정보를 등록하거나 업데이트합니다.'

    def handle(self, *args, **options):
        # 1. 사이트 설정 확인 (ID=1)
        # 도메인과 이름을 실제 사용 환경에 맞게 강제 업데이트합니다.
        site, _ = Site.objects.update_or_create(
            id=1, 
            defaults={'domain': '127.0.0.1:8000', 'name': '127.0.0.1:8000'}
        )

        # 2. 구글 설정 (업데이트 또는 생성)
        google_id = os.getenv('GOOGLE_CLIENT_ID')
        google_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        print(f"DEBUG: GOOGLE_CLIENT_ID is {google_id}")

        if google_id and google_secret:
            app, created = SocialApp.objects.update_or_create(
                provider='google',
                defaults={
                    'name': 'Google', 
                    'client_id': google_id, 
                    'secret': google_secret
                }
            )
            app.sites.add(site) # 사이트 연결 필수
            status = "생성" if created else "업데이트"
            self.stdout.write(self.style.SUCCESS(f'Google 앱 {status} 완료'))
        else:
            self.stdout.write(self.style.ERROR('Google 환경변수를 찾을 수 없습니다.'))

        # 3. 네이버 설정 (있을 경우)
        naver_id = os.getenv('NAVER_CLIENT_ID')
        naver_secret = os.getenv('NAVER_CLIENT_SECRET')
        
        if naver_id and naver_secret:
            app, created = SocialApp.objects.update_or_create(
                provider='naver',
                defaults={
                    'name': 'Naver', 
                    'client_id': naver_id, 
                    'secret': naver_secret
                }
            )
            app.sites.add(site)
            status = "생성" if created else "업데이트"
            self.stdout.write(self.style.SUCCESS(f'Naver 앱 {status} 완료'))
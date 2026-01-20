# Piro24_CardGame_1
피로그래밍 24기 4주차 카드게임 1조 레포입니다.

## 🚀 시작하기

### 환경 설정
⚠️ 모든 명령은 `manage.py`가 있는 프로젝트 루트에서 실행해주세요.

1. **가상환경 생성 및 활성화**
```bash
python -m venv venv
source venv\Scripts\activate   # Windows
# source venv/bin/activate    # macOS/Linux

```

2. **의존성 설치**
```bash
pip install django
```

3. **데이터베이스 마이그레이션**
```bash
python manage.py migrate
```

4. **관리자 계정 생성 (선택)**
```bash
python manage.py createsuperuser
```

5. **서버 실행**
```bash
python manage.py runserver
```


## 📁 프로젝트 구조

```
Piro24_CardGame_1/
├── config/          # 메인 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── accounts/        # 로그인/회원가입 앱
│   ├── models.py      # 모델
│   ├── views.py       # 뷰 로직
│   ├── forms.py       # Django Forms
│   ├── urls.py        # URL 라우팅
│   ├── admin.py       # 관리자 페이지 설정
│   └── templates/     # HTML 템플릿
├── games/        # 게임 로직 앱
│   ├── models.py      # 모델
│   ├── views.py       # 뷰 로직
│   ├── forms.py       # Django Forms
│   ├── urls.py        # URL 라우팅
│   ├── admin.py       # 관리자 페이지 설정
│   └── templates/     # HTML 템플릿
├── templates/          # 공통 템플릿
│   └── base.html      # 기본 레이아웃
│   └── ...
├── manage.py
└── README.md
```
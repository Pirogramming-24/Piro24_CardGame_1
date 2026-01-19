### 1. 빌드 단계
FROM python:3.12 AS builder


WORKDIR /usr/src/app

# 캐시 효율을 위해 requirements.txt만 먼저 복사
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . .

### 2. 실행 단계
FROM python:3.12-slim AS runtime

# Django에서 MySQL을 사용하기 위해 필요한 libmariadb3를 설치합니다.
# libmariadb3는 mysqlclient 실행용(Runtime) 패키지로 매우 가볍습니다.
RUN apt-get update && apt-get install -y \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# 파이썬 출력을 터미널에 즉시 표시 (로그 확인용)
ENV PYTHONUNBUFFERED=1

# 빌드 단계에서 설치된 3.12 라이브러리와 바이너리 복사 (경로 수정됨)
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/src/app /usr/src/app

# 컨테이너 실행 명령 (JSON 형식을 더 권장하지만 일단 작동하도록 유지)
CMD sh -c "python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    python manage.py runserver 0.0.0.0:8000"

EXPOSE 8000
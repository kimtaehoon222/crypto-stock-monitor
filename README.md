# crypto-stock-monitor

구조
crypto-stock-monitor/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 시작점
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── assets.py       # 종목/코인 API
│   │   │   ├── prices.py       # 가격 데이터 API
│   │   │   ├── users.py        # 사용자 관리 API
│   │   │   └── alerts.py       # 알림 관리 API
│   │   └── dependencies.py     # 공통 의존성
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # 설정 관리
│   │   ├── database.py         # DB 연결
│   │   ├── security.py         # JWT 인증
│   │   └── exceptions.py       # 예외 처리
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # 사용자 모델
│   │   ├── asset.py            # 자산 모델
│   │   ├── price.py            # 가격 데이터 모델
│   │   └── alert.py            # 알림 모델
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # 사용자 스키마
│   │   ├── asset.py            # 자산 스키마
│   │   ├── price.py            # 가격 스키마
│   │   └── alert.py            # 알림 스키마
│   ├── services/
│   │   ├── __init__.py
│   │   ├── price_fetcher.py    # 외부 API 호출
│   │   ├── user_service.py     # 사용자 비즈니스 로직
│   │   ├── alert_service.py    # 알림 비즈니스 로직
│   │   └── scheduler.py        # 주기적 작업 스케줄러
│   └── utils/
│       ├── __init__.py
│       ├── crypto_apis.py      # 암호화폐 API 연동
│       ├── stock_apis.py       # 주식 API 연동
│       └── notifications.py    # 알림 발송
├── alembic/                    # DB 마이그레이션
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── __init__.py
│   ├── test_assets.py
│   ├── test_prices.py
│   └── test_users.py
├── .env                        # 환경변수
├── .gitignore
├── alembic.ini                 # Alembic 설정
├── docker-compose.yml          # Docker 설정
├── pyproject.toml              # uv 패키지 설정
└── README.md
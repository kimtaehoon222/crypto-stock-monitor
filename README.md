# crypto-stock-monitor

## 📁 프로젝트 구조

```
crypto-stock-monitor/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI 앱 시작점
│   └── api/
│       ├── __init__.py
│       ├── endpoints/
│       │   ├── __init__.py
│       │   ├── assets.py          # 종목/코인 API
│       │   ├── prices.py          # 가격 데이터 API
│       │   ├── alerts.py          # 알림 관리 API
│       │   └── users.py           # 사용자 관리 API
│       └── dependencies.py        # 공통 의존성
├── core/
│   ├── __init__.py
│   ├── config.py                  # 설정 관리
│   ├── database.py                # DB 연결
│   └── security.py                # JWT 인증
├── models/
│   ├── __init__.py
│   ├── asset.py                   # 자산 모델
│   ├── price.py                   # 가격 데이터 모델
│   ├── alert.py                   # 알림 모델
│   └── user.py                    # 사용자 모델
├── services/
│   ├── __init__.py
│   ├── price_fetcher.py           # 외부 API 호출
│   ├── user_service.py            # 사용자 비즈니스 로직
│   ├── alert_service.py           # 알림 비즈니스 로직
│   └── scheduler.py               # 주기적 작업 스케줄러
├── utils/
│   ├── __init__.py
│   ├── crypto_apis.py             # 암호화폐 API 연동
│   └── stock_apis.py              # 주식 API 연동
├── tests/
├── .env                           # 환경변수
├── .gitignore
├── alembic.ini                    # Alembic 설정
├── docker-compose.yml             # Docker 설정
├── pyproject.toml                 # 패키지 설정
└── README.md
```
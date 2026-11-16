# Hupy — Hypixel SkyBlock Parser

Сервис для парсинга и хранения цен **Hypixel SkyBlock**: Bazaar и Auction House.
Собирает данные из [Hypixel API v2](https://api.hypixel.net/), агрегирует их
и отдаёт через REST API с кэшированием в Redis.

# Содержание

- [Архитектура](#архитектура)
- [Возможности](#возможности)
- [Быстрый старт](#быстрый-старт)
- [Конфигурация](#конфигурация)
- [API](#api)
- [Структура проекта](#структура-проекта)
- [Как это работает](#как-это-работает)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [Миграции](#миграции)
- [Известные ограничения](#известные-ограничения)

# Архитектура

Проект разделён на два независимых процесса, которые общаются через
PostgreSQL и Redis:
┌─────────────┐ ┌─────────────┐
│ Hypixel │◄───────│ worker │ ← APScheduler + Redis Lock
│ API v2 │ │ │ раз в 5/5/2 минуты
└─────────────┘ └──────┬──────┘
│
┌──────▼──────┐
│ PostgreSQL │ (timescaledb)
└──────▲──────┘
│
┌─────────────┐ ┌──────┴──────┐
│ Клиент │◄───────│ app │ ← FastAPI + uvicorn
│ (frontend) │ │ │
└─────────────┘ └─────────────┘
│
┌──────▼──────┐
│ Redis │ (cache + lock)
└─────────────┘
- **`worker`** — отдельный процесс-сборщик. Запускается **в одном экземпляре**,
  крутит три джобы по расписанию и защищён `Redis Lock` от параллельных
  запусков на случай рестарта/повторного деплоя.
- **`app`** — FastAPI, отдаёт REST API, работает за uvicorn (2 воркера).
  К Hypixel **не** обращается, читает только из БД.

---

## Возможности

### Bazaar
- Синхронизация `quick_status` (buy/sell price + volume) по всем продуктам.
- Автоматическая категоризация: `main → sub → [sub-sub] → items`.
- Автокомплит по `product_id` с ранжированием (точное → префикс → подстрока).
- История цен по продукту.
- Дерево категорий с кэшем.

### Auction
- Синхронизация `lowest BIN` (только BIN-лоты) с группировкой по `(item_name, tier)`.
- История `lowest_bin` и `listings_count`.
- Факты продаж из `/skyblock/auctions_ended` — источник средней цены продажи.
- Рейтинг (`COMMON`…`VERY SPECIAL`) для sales извлекается из цвета NBT.
- Статистика: средняя цена продажи, количество покупок, среднее число
  активных выставлений за период.
- Автокомплит по `item_name` + `tier`.

### Инфраструктура
- Redis-кэш на всех read-эндпоинтах.
- Redis Lock для синхронизаций (безопасно при рестарте воркера).
- Retry с экспоненциальным backoff для всех запросов к Hypixel.
- Асинхронный стек: SQLAlchemy 2.x async + asyncpg + httpx.
- Миграции через Alembic (async).
- Unit- и service-тесты на pytest + httpx.MockTransport.

---

## Быстрый старт

### Docker Compose (рекомендуется)

```bash
git clone https://github.com/<ваш-ник>/Hupy.git
cd Hupy

cp .env.example .env
# откройте .env и впишите HYPIXEL_API_KEY

docker compose up -d --build
```
Сервис будет доступен:
API: http://localhost:8000
Swagger UI: http://localhost:8000/docs
Health: http://localhost:8000/health

Логи:

bash
docker compose logs -f worker
docker compose logs -f app
Остановка:

bash
docker compose down            # без удаления volume'ов
docker compose down -v         # с удалением БД и кэша
Локальная разработка
Нужны: Python 3.12+, PostgreSQL 16, Redis 7.

bash
# 1. Инфраструктура в Docker
docker compose up -d postgres redis

# 2. Виртуальное окружение
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 3. Миграции
alembic upgrade head

# 4. Запуск API
uvicorn main:app --reload --port 8000

# 5. Запуск воркера (в отдельном терминале)
python -m worker
Конфигурация
Все настройки читаются из .env (см. .env.example).

Переменная	Обязательна	По умолчанию	Описание
HYPIXEL_API_KEY	✅	—	API-ключ Hypixel (без него возможен 429)
DATABASE_URL		postgresql+asyncpg://skyblock:skyblock@localhost:5432/skyblock	DSN PostgreSQL
REDIS_URL		redis://localhost:6379/0	DSN Redis
BAZAAR_FETCH_INTERVAL		300	Интервал синхронизации Bazaar, сек
AUCTION_FETCH_INTERVAL		300	Интервал синхронизации Auction, сек
SALES_FETCH_INTERVAL		120	Интервал синхронизации sales, сек
POSTGRES_USER		skyblock	(только docker-compose)
POSTGRES_PASSWORD		skyblock	(только docker-compose)
APP_VERSION		latest	Тег образа для docker-compose
⚠️ HYPIXEL_API_KEY Без него Hypixel отдаёт 429 после нескольких запросов в минуту, и синхронизация будет
работать нестабильно.

API
Базовый префикс: /

Bazaar
Метод	             Путь                    Описание 
GET	/bazaar/search?search=&limit=20	Автокомплит по продуктам
GET	/bazaar/{product_id}/history?limit=100	История цен по продукту
Пример:

bash
curl "http://localhost:8000/bazaar/search?search=carrot&limit=5"
curl "http://localhost:8000/bazaar/CARROT_ITEM/history?limit=10"
Auction
Метод	            Путь                     Описание
GET	/auction/search?search=&limit=20	Автокомплит по предметам
GET	/auction/history?item_name=&tier=&limit=100	История lowest_bin
GET	/auction/stats?item_name=&tier=&days=7	Статистика продаж
Пример:

bash
curl "http://localhost:8000/auction/history?item_name=Hyperion&tier=LEGENDARY&limit=10"
curl "http://localhost:8000/auction/stats?item_name=Hyperion&days=7"
/auction/stats возвращает:

json
{
  "item_name": "Hyperion",
  "tier": "LEGENDARY",
  "available_tiers": ["EPIC", "LEGENDARY"],
  "period_days": 7,
  "avg_sale_price": 1050000000,
  "sales_count": 42,
  "avg_listings": 3.5
}
Categories
Метод	  Путь	      Описание
GET	/categories/	Дерево main → subcategories

Метод	Путь	Описание
GET	/health	Статус сервиса
GET	/docs	Swagger UI
GET	/redoc	ReDoc
Структура проекта
text
Hupy/
├── api/
│   ├── dependencies.py          # DI: repo-фабрики
│   └── routes/
│       ├── bazaar.py            # /bazaar/*
│       ├── auction.py           # /auction/*
│       └── categories.py        # /categories/
├── core/
│   ├── config.py                # Pydantic Settings
│   ├── database.py              # async engine + session
│   ├── redis_client.py          # Redis pool
│   ├── hypixel_client.py        # HTTP-клиент + retry + NBT
│   ├── scheduler.py             # APScheduler + Redis Lock
│   ├── bootstrap.py             # seed категорий + кэш
│   ├── category_cache.py        # (main, sub) → sub_category_id
│   └── utils/
│       ├── normalize_item_name.py
│       ├── normalize_product_id.py
│       └── category_utils.py
├── models/
│   ├── category.py              # MainCategory, SubCategory
│   ├── price.py                 # BazaarPrice, AuctionPrice, AuctionSale
│   ├── seed_data.py             # дерево категорий Bazaar
│   ├── product_categories.py    # slugify/overrides/prefix-rules
│   └── product_id_manual.py     # ручной маппинг редких предметов
├── repositories/
│   ├── base.py
│   ├── bazaar_repo.py
│   └── auction_repo.py
├── services/
│   ├── bazaar_service.py        # fetch → transform → save
│   ├── auction_service.py
│   └── categories_service.py    # seed
├── schemas/
│   ├── enums.py                 # Tier
│   └── schemas.py               # Pydantic response-модели
├── alembic/                     # миграции
├── tests/
│   ├── unit/
│   ├── services/
│   └── repositories/
├── main.py                      # FastAPI app
├── worker.py                    # процесс-сборщик
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml
└── requirements.txt

Как это работает:
Bazaar
worker каждые BAZAAR_FETCH_INTERVAL секунд дёргает /skyblock/bazaar.

Для каждого product_id определяется категория:

PRODUCT_TO_CATEGORY (slugify + явные overrides + книги зачарований);

MANUAL_CATEGORIES (ручной словарь);

префиксные/суффиксные/подстрочные правила;

fallback → ("Unknown", "Uncategorized").

(main, sub) → sub_category_id берётся из in-memory кэша,
который строится при старте воркера (bootstrap.seed_and_cache).

quick_status сохраняется в bazaar_prices с sub_category_id.

Auction
worker постранично тянет /skyblock/auctions (до totalPages),
между страницами — пауза PAGE_DELAY=0.3s.

Из всех BIN-лотов считаются min(starting_bid) и count по
ключу (item_name, tier). Имя нормализуется: §-коды, [Lvl N],
символы ✪ ◆ — срезаются.

Пишется одна запись в auction_prices (PK: item_name, tier, timestamp
с date_trunc('minute', now()) — одна запись на минуту).

Отдельная джоба тянет /skyblock/auctions_ended — это факты продаж.
item_name и tier извлекаются из base64-gzip-NBT item_bytes
(поле display.Name), редкость — по цвету (§6 → LEGENDARY и т.д.).

auction_sales — append-only, PK auction_uuid (idempotent через
ON CONFLICT DO NOTHING).

Кэширование
bazaar:search:* — 30 сек

bazaar:{pid}:* — 30 сек

auction:search:* — 60 сек

auction:history:* — 60 сек

auction:stats:* — 60 сек

categories:tree — 3600 сек

Ключи строятся по нормализованному входу — "Hyperion" и
"hyperion " дают один и тот же кэш.

Redis Lock
Все три джобы обёрнуты в @with_redis_lock(name). Lock TTL = 900 сек,
снятие — атомарно через Lua (GET + DEL только если наш token).
Это защищает от:

параллельного запуска на двух worker-контейнерах;

повторного запуска после рестарта;

misfire от планировщика.

Разработка
Pre-commit
bash
ruff check .
ruff format .
mypy .
Обновление списка категорий
Дерево категорий Bazaar лежит в models/seed_data.py. После правок:

bash
# пересоздать категории в БД
python -c "import asyncio; from core.bootstrap import seed_and_cache; asyncio.run(seed_and_cache())"
Аудит неклассифицированных предметов
bash
python -m scripts.audit_unknown
Покажет product_id, которые не попали ни в PRODUCT_TO_CATEGORY,
ни в MANUAL_CATEGORIES, ни в паттерны. Их нужно добавить в
models/product_id_manual.py.

Очистка кэша
bash
docker compose exec redis redis-cli FLUSHDB
Тестирование
bash
# все тесты
pytest

# только unit (без БД)
pytest tests/unit -v

# с покрытием
pytest --cov=core --cov=services --cov=repositories --cov-report=term-missing
Структура:

tests/unit/ — нормализация, slugify, _tier_from_colored_name,
expand_book_range, _get_with_retry (через httpx.MockTransport).

tests/services/ — fetch_and_save с фейковым клиентом и repo.

tests/repositories/ — на реальном Postgres через testcontainers.

⚠️ tests/repositories/ требует Docker. Если на CI он недоступен —
используйте маркер @pytest.mark.repo и запускайте pytest -m "not repo".

Миграции
bash
# применить все
alembic upgrade head

# откатить последнюю
alembic downgrade -1

# новая миграция (autogenerate)
alembic revision --autogenerate -m "add new column"
Миграции async — alembic/env.py использует async_engine_from_config.
URL берётся из settings.database_url (не из alembic.ini).

Известные ограничения
auctions_ended и рейтинг. Hypixel не отдаёт tier в
/skyblock/auctions_ended, поэтому редкость вытаскивается из
display.Name NBT через §-коды. Для некоторых предметов
(например, кастомные ✪-звёзды в имени) tier может быть None.
В БД auction_sales.tier — nullable.

auction_prices.tier — NOT NULL DEFAULT '' (не NULL), чтобы
PK (item_name, tier, timestamp) не ломался. В available_tiers
пустая строка должна фильтроваться (см. get_stats), иначе
фронт увидит мусорный тир.

auction_sales — append-only. Дедупликация через
ON CONFLICT (auction_uuid) DO NOTHING; при повторной синхронизации
старые записи не перезаписываются.

/bazaar/{product_id}/history возвращает историю по
product_id в том виде, в котором он лежит в БД. Входной параметр
нормализуется через normalize_product_id, но хранимые значения —
как их отдаёт Hypixel (UPPER_SNAKE_CASE).

/auction/history и /auction/stats сейчас ищут item_name
в БД с сохранённым регистром (WHERE item_name = 'Hyperion').
Входной "HYPERION" вернёт пустой результат. Если нужно
регистронезависимое сравнение — используйте func.lower(...).

Redis Lock TTL (900 сек) > интервала джоб (120–300 сек). Если
воркер упадёт между SET NX и DEL, lock будет висеть 15 минут —
итерации пропустятся. Это осознанный компромисс в пользу
безопасности от параллельных запусков.

Лицензия
MIT 

Благодарности
Hypixel API — источник данных.

FastAPI,
SQLAlchemy,
APScheduler,
nbtlib — стек проекта.

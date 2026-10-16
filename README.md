# Каталог видеоигр (вариант 37)

Многокомпонентное приложение на Docker Compose.
**Web-сервис:** каталог видеоигр — поиск по жанру и минимальным системным требованиям (ОЗУ, CPU, диск, видеокарта).
**БД:** игровая библиотека пользователя (PostgreSQL) со статусами «В планах / Играю / Пройдена».

## Архитектура

| Сервис | Технологии | Назначение |
|---|---|---|
| frontend | nginx + HTML/CSS/JS | UI, проксирует `/api` на backend (порт хоста **8081**) |
| backend | Python, Flask | REST API, CRUD к БД, интеграция с web-service |
| db | PostgreSQL 16 | таблица `library`, init через `db/init.sql`, volume `db_data` |
| web-service | Python, Flask | эмулятор API каталога игр (25 игр) |

Кнопки интерфейса: **«Найти в каталоге»** (запрос к web-service через backend, с возможностью добавить игру в библиотеку) и **«Моя библиотека»** (данные из БД, смена статуса, удаление).

## Запуск

```bash
cp .env.example .env   # опционально
docker compose up -d --build
```

Открыть http://localhost:8081. Остановка: `docker compose down` (данные сохраняются в volume; `-v` — удалить).

## API backend
- `GET /api/library`, `POST /api/library`, `PUT /api/library/<id>` `{status}`, `DELETE /api/library/<id>`
- `GET /api/catalog?genre=&q=&ram=&cpu=&disk=&gpu_tier=`, `GET /api/genres`

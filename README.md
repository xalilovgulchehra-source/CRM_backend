# Salon CRM Backend

Sartaroshxona/salon CRM backend API — Django + Django REST Framework asosida.

## Texnologiyalar

- Python 3.11+
- Django 5+
- Django REST Framework
- PostgreSQL
- JWT autentifikatsiya (djangorestframework-simplejwt)
- CamelCase JSON javoblar (djangorestframework-camel-case)

## O'rnatish

```bash
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Dependencies o'rnatish
pip install -r requirements.txt

# .env faylini yaratish
cp .env.example .env
# .env faylini to'ldiring

# Migratsiyalar
python manage.py migrate

# Server ishga tushirish
python manage.py runserver
```

## API Endpointlar

### Autentifikatsiya
- `POST /api/auth/register/` — Ro'yxatdan o'tish
- `POST /api/auth/login/` — Kirish
- `GET /api/auth/me/` — Joriy foydalanuvchi

### Mijozlar
- `GET /api/clients/` — Barcha mijozlar (?q= bilan qidirish)
- `GET /api/clients/{id}/` — Bitta mijoz
- `POST /api/clients/` — Yangi mijoz qo'shish
- `PUT /api/clients/{id}/` — Mijozni yangilash
- `DELETE /api/clients/{id}/` — Mijozni o'chirish

### Xizmatlar
- `GET /api/services/` — Barcha xizmatlar
- `POST /api/services/` — Yangi xizmat qo'shish
- `PUT /api/services/{id}/` — Xizmatni yangilash
- `DELETE /api/services/{id}/` — Xizmatni o'chirish

### Navbatlar
- `GET /api/bookings/` — Barcha navbatlar (?status=PENDING kabi filtr)
- `POST /api/bookings/` — Yangi navbat yaratish
- `PUT /api/bookings/{id}/` — Navbatni yangilash
- `DELETE /api/bookings/{id}/` — Navbatni o'chirish

### Dashboard
- `GET /api/dashboard/stats/` — Statistika

## Render'ga Deploy

1. Repositoryni GitHub'ga yuklang
2. Render'da yangi Web Service yarating
3. Build Command: `bash build.sh`
4. Start Command: `gunicorn config.wsgi`
5. Environment Variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `FRONTEND_URL`
   - `DEBUG=False`

## Migratsiyalar (Deploy vaqtida)

`build.sh` avtomatik migratsiyalarni ishga tushiradi. Qo'lda ishga tushirish uchun:

```bash
python manage.py migrate
```

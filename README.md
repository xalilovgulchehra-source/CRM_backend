# Salon CRM Backend

Sartaroshxona/salon CRM tizimi uchun REST API backend.

##Texnologiyalar

- Node.js + Express
- PostgreSQL + Prisma ORM
- JWT autentifikatsiya
- Zod validatsiya
- TypeScript

## O'rnatish

```bash
# Bog'lanishlar
npm install

# Muhit o'zgaruvchilarini yarating
cp .env.example .env
# .env faylini to'ldiring

# Prisma migratsiyasi
npx prisma migrate dev

# Ishga tushirish (rivojlantirish)
npm run dev

# Ishlab chiqarish
npm run build
npm start
```

## Muhit o'zgaruvchilari

| O'zgaruvchi | Tavsif | Misol |
|---|---|---|
| `DATABASE_URL` | PostgreSQL ulanish manzili | `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET` | JWT token kaliti | `kamida-32-belgi` |
| `PORT` | Server porti | `3000` |
| `FRONTEND_URL` | Frontend domeni (CORS) | `https://your-app.onrender.com` |

## API Endpointlar

### Autentifikatsiya
- `POST /api/auth/register` — Ro'yxatdan o'tish
- `POST /api/auth/login` — Tizimga kirish
- `GET /api/auth/me` — Joriy foydalanuvchi (🔒)

### Mijozlar (🔒 barchasi)
- `GET /api/clients?q=` — Barcha mijozlar (qidiruv bilan)
- `GET /api/clients/:id` — Bitta mijoz
- `POST /api/clients` — Yangi mijoz
- `PUT /api/clients/:id` — Mijozni yangilash
- `DELETE /api/clients/:id` — Mijozni o'chirish

### Xizmatlar (🔒 barchasi)
- `GET /api/services` — Barcha xizmatlar
- `GET /api/services/:id` — Bitta xizmat
- `POST /api/services` — Yangi xizmat
- `PUT /api/services/:id` — Xizmatni yangilash
- `DELETE /api/services/:id` — Xizmatni o'chirish

### Navbatlar (🔒 barchasi)
- `GET /api/bookings?from=&to=&status=` — Barcha navbatlar (sana filtri)
- `GET /api/bookings/:id` — Bitta navbat
- `POST /api/bookings` — Yangi navbat
- `PUT /api/bookings/:id` — Navbatni yangilash
- `DELETE /api/bookings/:id` — Navbatni o'chirish

### Dashboard (🔒)
- `GET /api/dashboard/stats` — Statistika

🔒 = JWT token talab qilinadi: `Authorization: Bearer <token>`

## Render'ga Deploy

1. PostgreSQL bazasini yarating (Render → New → PostgreSQL)
2. Backend xizmasini yarating (Render → New → Web Service)
3. Environment o'zgaruvchilarini kiriting:

```
DATABASE_URL=<Render PostgreSQL URL>
JWT_SECRET=<kamida-32-belgi>
FRONTEND_URL=<frontend domeni>
```

4. Build command: `npm install && npm run build`
5. Start command: `npm start`
6. Deploy

Deploy keyin migratsiyani avtomatik ishga tushiring:
- Render Service → Shell yoki
- `npm run prisma:migrate` buyrug'ini ishga tushiring

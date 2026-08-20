import { Router, Response } from "express";
import { PrismaClient } from "@prisma/client";
import { bookingSchema, BookingInput } from "../validations";
import { authMiddleware, AuthRequest } from "../middleware/auth";

const router = Router();
const prisma = new PrismaClient();

router.use(authMiddleware);

// GET /api/bookings — sana filtri bilan: ?from=&to=&status=
router.get("/", async (req: AuthRequest, res: Response) => {
  try {
    const { from, to, status } = req.query;

    const where: any = { userId: req.userId! };

    if (from || to) {
      where.date = {};
      if (from) where.date.gte = new Date(from as string);
      if (to) where.date.lte = new Date(to as string);
    }

    if (status) {
      where.status = status;
    }

    const navbatlar = await prisma.booking.findMany({
      where,
      include: { client: true, service: true },
      orderBy: { date: "asc" },
    });

    res.json({ navbatlar, soni: navbatlar.length });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Navbatlarni olishda xatolik" });
  }
});

// GET /api/bookings/:id
router.get("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const navbat = await prisma.booking.findFirst({
      where: { id, userId: req.userId! },
      include: { client: true, service: true },
    });

    if (!navbat) {
      res.status(404).json({ xato: "Navbat topilmadi" });
      return;
    }

    res.json({ navbat });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Navbatni olishda xatolik" });
  }
});

// POST /api/bookings
router.post("/", async (req: AuthRequest, res: Response) => {
  try {
    const data: BookingInput = bookingSchema.parse(req.body);

    const mijoz = await prisma.client.findFirst({
      where: { id: data.clientId, userId: req.userId! },
    });
    if (!mijoz) {
      res.status(404).json({ xato: "Mijoz topilmadi" });
      return;
    }

    const xizmat = await prisma.service.findFirst({
      where: { id: data.serviceId, userId: req.userId! },
    });
    if (!xizmat) {
      res.status(404).json({ xato: "Xizmat topilmadi" });
      return;
    }

    const navbat = await prisma.booking.create({
      data: {
        date: new Date(data.date),
        status: data.status || "PENDING",
        notes: data.notes,
        price: data.price,
        clientId: data.clientId,
        serviceId: data.serviceId,
        userId: req.userId!,
      },
      include: { client: true, service: true },
    });

    await prisma.client.update({
      where: { id: data.clientId },
      data: { lastVisit: new Date() },
    });

    res.status(201).json({ navbat });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Navbatni yaratishda xatolik" });
  }
});

// PUT /api/bookings/:id
router.put("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.booking.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Navbat topilmadi" });
      return;
    }

    const data = bookingSchema.partial().parse(req.body);

    const navbat = await prisma.booking.update({
      where: { id },
      data: {
        ...(data.date && { date: new Date(data.date) }),
        ...(data.status && { status: data.status }),
        ...(data.notes !== undefined && { notes: data.notes }),
        ...(data.price && { price: data.price }),
        ...(data.clientId && { clientId: data.clientId }),
        ...(data.serviceId && { serviceId: data.serviceId }),
      },
      include: { client: true, service: true },
    });

    res.json({ navbat });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Navbatni yangilashda xatolik" });
  }
});

// DELETE /api/bookings/:id
router.delete("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.booking.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Navbat topilmadi" });
      return;
    }

    await prisma.booking.delete({ where: { id } });
    res.json({ xabar: "Navbat muvaffaqiyatli o'chirildi" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Navbatni o'chirishda xatolik" });
  }
});

export default router;

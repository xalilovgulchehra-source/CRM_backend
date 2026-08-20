import { Router, Response } from "express";
import { PrismaClient } from "@prisma/client";
import { clientSchema, ClientInput } from "../validations";
import { authMiddleware, AuthRequest } from "../middleware/auth";

const router = Router();
const prisma = new PrismaClient();

router.use(authMiddleware);

// GET /api/clients — barcha mijozlar, ?q= bilan qidirish
router.get("/", async (req: AuthRequest, res: Response) => {
  try {
    const q = req.query.q as string | undefined;

    const where: any = { userId: req.userId! };

    if (q) {
      where.OR = [
        { fullName: { contains: q, mode: "insensitive" } },
        { phone: { contains: q, mode: "insensitive" } },
      ];
    }

    const mijozlar = await prisma.client.findMany({
      where,
      orderBy: { createdAt: "desc" },
      include: { _count: { select: { bookings: true } } },
    });

    res.json({ mijozlar, soni: mijozlar.length });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Mijozlarni olishda xatolik" });
  }
});

// GET /api/clients/:id
router.get("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mijoz = await prisma.client.findFirst({
      where: { id, userId: req.userId! },
      include: { bookings: { include: { service: true }, orderBy: { date: "desc" } } },
    });

    if (!mijoz) {
      res.status(404).json({ xato: "Mijoz topilmadi" });
      return;
    }

    res.json({ mijoz });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Mijozni olishda xatolik" });
  }
});

// POST /api/clients
router.post("/", async (req: AuthRequest, res: Response) => {
  try {
    const data: ClientInput = clientSchema.parse(req.body);

    const mijoz = await prisma.client.create({
      data: { ...data, userId: req.userId! },
    });

    res.status(201).json({ mijoz });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Mijozni yaratishda xatolik" });
  }
});

// PUT /api/clients/:id
router.put("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.client.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Mijoz topilmadi" });
      return;
    }

    const data = clientSchema.partial().parse(req.body);

    const mijoz = await prisma.client.update({
      where: { id },
      data,
    });

    res.json({ mijoz });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Mijozni yangilashda xatolik" });
  }
});

// DELETE /api/clients/:id
router.delete("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.client.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Mijoz topilmadi" });
      return;
    }

    await prisma.client.delete({ where: { id } });
    res.json({ xabar: "Mijoz muvaffaqiyatli o'chirildi" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Mijozni o'chirishda xatolik" });
  }
});

export default router;

import { Router, Response } from "express";
import { PrismaClient } from "@prisma/client";
import { serviceSchema, ServiceInput } from "../validations";
import { authMiddleware, AuthRequest } from "../middleware/auth";

const router = Router();
const prisma = new PrismaClient();

router.use(authMiddleware);

// GET /api/services
router.get("/", async (req: AuthRequest, res: Response) => {
  try {
    const xizmatlar = await prisma.service.findMany({
      where: { userId: req.userId! },
      orderBy: { createdAt: "desc" },
    });

    res.json({ xizmatlar, soni: xizmatlar.length });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Xizmatlarni olishda xatolik" });
  }
});

// GET /api/services/:id
router.get("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const xizmat = await prisma.service.findFirst({
      where: { id, userId: req.userId! },
    });

    if (!xizmat) {
      res.status(404).json({ xato: "Xizmat topilmadi" });
      return;
    }

    res.json({ xizmat });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Xizmatni olishda xatolik" });
  }
});

// POST /api/services
router.post("/", async (req: AuthRequest, res: Response) => {
  try {
    const data: ServiceInput = serviceSchema.parse(req.body);

    const xizmat = await prisma.service.create({
      data: { ...data, userId: req.userId! },
    });

    res.status(201).json({ xizmat });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Xizmatni yaratishda xatolik" });
  }
});

// PUT /api/services/:id
router.put("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.service.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Xizmat topilmadi" });
      return;
    }

    const data = serviceSchema.partial().parse(req.body);

    const xizmat = await prisma.service.update({
      where: { id },
      data,
    });

    res.json({ xizmat });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Xizmatni yangilashda xatolik" });
  }
});

// DELETE /api/services/:id
router.delete("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.status(400).json({ xato: "Noto'g'ri ID" });
      return;
    }

    const mavjud = await prisma.service.findFirst({ where: { id, userId: req.userId! } });
    if (!mavjud) {
      res.status(404).json({ xato: "Xizmat topilmadi" });
      return;
    }

    await prisma.service.delete({ where: { id } });
    res.json({ xabar: "Xizmat muvaffaqiyatli o'chirildi" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Xizmatni o'chirishda xatolik" });
  }
});

export default router;

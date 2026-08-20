import { Router, Response } from "express";
import { PrismaClient } from "@prisma/client";
import { authMiddleware, AuthRequest } from "../middleware/auth";

const router = Router();
const prisma = new PrismaClient();

router.use(authMiddleware);

// GET /api/dashboard/stats
router.get("/stats", async (req: AuthRequest, res: Response) => {
  try {
    const now = new Date();

    const bugunBoshlanishi = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const bugunTugashi = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);

    const oyBoshlanishi = new Date(now.getFullYear(), now.getMonth(), 1);
    const oyTugashi = new Date(now.getFullYear(), now.getMonth() + 1, 1);

    const [
      umumiyMijozlar,
      bugungiNavbatlar,
      kelayotganNavbatlar,
      oylikDaromad,
      bajarilganNavbatlar,
      bekorQilinganNavbatlar,
    ] = await Promise.all([
      prisma.client.count({ where: { userId: req.userId! } }),

      prisma.booking.findMany({
        where: {
          userId: req.userId!,
          date: { gte: bugunBoshlanishi, lt: bugunTugashi },
        },
        include: { client: true, service: true },
        orderBy: { date: "asc" },
      }),

      prisma.booking.findMany({
        where: {
          userId: req.userId!,
          date: { gt: now },
          status: { in: ["PENDING", "CONFIRMED"] },
        },
        include: { client: true, service: true },
        orderBy: { date: "asc" },
        take: 10,
      }),

      prisma.booking.aggregate({
        where: {
          userId: req.userId!,
          date: { gte: oyBoshlanishi, lt: oyTugashi },
          status: { in: ["CONFIRMED", "DONE"] },
        },
        _sum: { price: true },
      }),

      prisma.booking.count({
        where: {
          userId: req.userId!,
          date: { gte: oyBoshlanishi, lt: oyTugashi },
          status: "DONE",
        },
      }),

      prisma.booking.count({
        where: {
          userId: req.userId!,
          date: { gte: oyBoshlanishi, lt: oyTugashi },
          status: "CANCELLED",
        },
      }),
    ]);

    res.json({
      umumiyMijozlar,
      bugungiNavbatlar: { navbatlar: bugungiNavbatlar, soni: bugungiNavbatlar.length },
      kelayotganNavbatlar,
      oylikDaromad: oylikDaromad._sum.price || 0,
      bajarilganNavbatlar,
      bekorQilinganNavbatlar,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Statistikani olishda xatolik" });
  }
});

export default router;

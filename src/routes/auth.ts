import { Router, Response } from "express";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { PrismaClient } from "@prisma/client";
import { registerSchema, loginSchema, RegisterInput, LoginInput } from "../validations";
import { authMiddleware, AuthRequest } from "../middleware/auth";

const router = Router();
const prisma = new PrismaClient();

router.post("/register", async (req, res: Response) => {
  try {
    const data: RegisterInput = registerSchema.parse(req.body);

    const mavjud = await prisma.user.findUnique({ where: { email: data.email } });
    if (mavjud) {
      res.status(409).json({ xato: "Bu email allaqachon ro'yxatdan o'tgan" });
      return;
    }

    const hashedPassword = await bcrypt.hash(data.password, 10);

    const user = await prisma.user.create({
      data: {
        email: data.email,
        password: hashedPassword,
        salonName: data.salonName,
        ownerName: data.ownerName,
        phone: data.phone,
      },
      select: { id: true, email: true, salonName: true, ownerName: true, phone: true, createdAt: true },
    });

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!, { expiresIn: "7d" });

    res.status(201).json({ token, foydalanuvchi: user });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Server xatosi" });
  }
});

router.post("/login", async (req, res: Response) => {
  try {
    const data: LoginInput = loginSchema.parse(req.body);

    const user = await prisma.user.findUnique({ where: { email: data.email } });
    if (!user) {
      res.status(401).json({ xato: "Email yoki parol noto'g'ri" });
      return;
    }

    const togrimi = await bcrypt.compare(data.password, user.password);
    if (!togrimi) {
      res.status(401).json({ xato: "Email yoki parol noto'g'ri" });
      return;
    }

    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!, { expiresIn: "7d" });

    res.json({
      token,
      foydalanuvchi: {
        id: user.id,
        email: user.email,
        salonName: user.salonName,
        ownerName: user.ownerName,
        phone: user.phone,
        createdAt: user.createdAt,
      },
    });
  } catch (err: any) {
    if (err.name === "ZodError") {
      res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: err.errors.map((e: any) => e.message) });
      return;
    }
    console.error(err);
    res.status(500).json({ xato: "Server xatosi" });
  }
});

router.get("/me", authMiddleware, async (req: AuthRequest, res: Response) => {
  try {
    const user = await prisma.user.findUnique({
      where: { id: req.userId! },
      select: { id: true, email: true, salonName: true, ownerName: true, phone: true, createdAt: true },
    });

    if (!user) {
      res.status(404).json({ xato: "Foydalanuvchi topilmadi" });
      return;
    }

    res.json({ foydalanuvchi: user });
  } catch (err) {
    console.error(err);
    res.status(500).json({ xato: "Server xatosi" });
  }
});

export default router;

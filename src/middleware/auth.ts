import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

export interface AuthRequest extends Request {
  userId?: number;
}

export function authMiddleware(req: AuthRequest, res: Response, next: NextFunction): void {
  const header = req.headers.authorization;

  if (!header || !header.startsWith("Bearer ")) {
    res.status(401).json({ xato: "Avtorizatsiya talab qilinadi" });
    return;
  }

  const token = header.split(" ")[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as { userId: number };
    req.userId = decoded.userId;
    next();
  } catch {
    res.status(401).json({ xato: "Noto'g'ri yoki muddati o'tgan token" });
  }
}

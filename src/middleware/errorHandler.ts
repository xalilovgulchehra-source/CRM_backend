import { Request, Response, NextFunction } from "express";
import { ZodError } from "zod";

export function errorHandler(err: Error, _req: Request, res: Response, _next: NextFunction): void {
  console.error("[XATO]", err);

  if (err instanceof ZodError) {
    const xatolar = err.errors.map((e) => e.message);
    res.status(400).json({ xato: "Validatsiya xatosi", tafsilotlar: xatolar });
    return;
  }

  res.status(500).json({ xato: "Ichki server xatosi" });
}

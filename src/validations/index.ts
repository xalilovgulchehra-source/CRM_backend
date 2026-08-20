import { z } from "zod";

export const registerSchema = z.object({
  email: z.string().email("Noto'g'ri email manzil"),
  password: z.string().min(6, "Parol kamida 6 ta belgi bo'lishi kerak"),
  salonName: z.string().min(1, "Salon nomi kiritilishi shart"),
  ownerName: z.string().min(1, "Egasi ismi kiritilishi shart"),
  phone: z.string().min(1, "Telefon raqami kiritilishi shart"),
});

export const loginSchema = z.object({
  email: z.string().email("Noto'g'ri email manzil"),
  password: z.string().min(1, "Parol kiritilishi shart"),
});

export const clientSchema = z.object({
  fullName: z.string().min(1, "Mijoz ismi kiritilishi shart"),
  phone: z.string().min(1, "Telefon raqami kiritilishi shart"),
  notes: z.string().optional(),
});

export const serviceSchema = z.object({
  name: z.string().min(1, "Xizmat nomi kiritilishi shart"),
  price: z.number().positive("Narx musbat son bo'lishi kerak"),
  durationMins: z.number().int().positive("Davomiylik musbat butun son bo'lishi kerak"),
});

export const bookingSchema = z.object({
  date: z.string().min(1, "Sana kiritilishi shart"),
  clientId: z.number().int().positive("Mijoz ID musbat son bo'lishi kerak"),
  serviceId: z.number().int().positive("Xizmat ID musbat son bo'lishi kerak"),
  price: z.number().positive("Narx musbat son bo'lishi kerak"),
  notes: z.string().optional(),
  status: z.enum(["PENDING", "CONFIRMED", "DONE", "CANCELLED"]).optional(),
});

export type RegisterInput = z.infer<typeof registerSchema>;
export type LoginInput = z.infer<typeof loginSchema>;
export type ClientInput = z.infer<typeof clientSchema>;
export type ServiceInput = z.infer<typeof serviceSchema>;
export type BookingInput = z.infer<typeof bookingSchema>;

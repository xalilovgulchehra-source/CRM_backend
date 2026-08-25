import dotenv from "dotenv";
dotenv.config();

import express from "express";
import cors from "cors";
import { PrismaClient } from "@prisma/client";
import { errorHandler } from "./middleware/errorHandler";
import authRoutes from "./routes/auth";
import clientRoutes from "./routes/clients";
import serviceRoutes from "./routes/services";
import bookingRoutes from "./routes/bookings";
import dashboardRoutes from "./routes/dashboard";

const app = express();
const prisma = new PrismaClient();
const PORT = process.env.PORT || 3000;

// CORS
const allowedOrigins = [
  "https://crm-frontend-nine-wheat.vercel.app",
  "https://crm-frontend-manzara.vercel.app",
  "http://localhost:3001",
];

app.use(
  cors({
    origin: function (origin, callback) {
      if (!origin || allowedOrigins.includes(origin)) {
        callback(null, true);
      } else {
        callback(new Error("CORS tomonidan bloklandi"));
      }
    },
    credentials: true,
  })
);
app.use(express.json());

// Health check
app.get("/", (_req, res) => {
  res.json({ holat: "faol", xizmat: "Salon CRM API", vaqt: new Date().toISOString() });
});

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/clients", clientRoutes);
app.use("/api/services", serviceRoutes);
app.use("/api/bookings", bookingRoutes);
app.use("/api/dashboard", dashboardRoutes);

// Error handler
app.use(errorHandler);

// Start server
async function main() {
  try {
    await prisma.$connect();
    console.log("PostgreSQL ga ulanildi");

    app.listen(PORT, () => {
      console.log(`Server ${PORT}-portda ishlayapti`);
    });
  } catch (err) {
    console.error("Serverni ishga tushirishda xatolik:", err);
    process.exit(1);
  }
}

main();

process.on("beforeExit", async () => {
  await prisma.$disconnect();
});

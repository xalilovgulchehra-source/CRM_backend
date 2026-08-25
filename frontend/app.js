const API = "https://crm-backend-api-zl4c.onrender.com";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function getUser() {
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
}

function setUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = "login.html";
}

function isLoggedIn() {
  return !!getToken();
}

function isCustomer() {
  const u = getUser();
  return u && u.role === "CUSTOMER";
}

function isOwner() {
  const u = getUser();
  return u && u.role === "OWNER";
}

async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, {
    headers,
    ...opts,
  });

  if (res.status === 401) {
    logout();
    return null;
  }

  const data = await res.json();
  if (!res.ok) throw { status: res.status, ...data };
  return data;
}

async function apiGet(path) {
  return api(path);
}

async function apiPost(path, body) {
  return api(path, { method: "POST", body: JSON.stringify(body) });
}

async function apiPut(path, body) {
  return api(path, { method: "PUT", body: JSON.stringify(body) });
}

async function apiDelete(path) {
  return api(path, { method: "DELETE" });
}

function toast(message, type = "info") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  const t = document.createElement("div");
  t.className = `toast toast-${type}`;
  t.textContent = message;
  container.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  return d.toLocaleDateString("uz-UZ", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatPrice(price) {
  if (!price && price !== 0) return "";
  return Number(price).toLocaleString("uz-UZ") + " so'm";
}

function statusBadge(status) {
  const map = {
    PENDING: ["Kutilmoqda", "badge-pending"],
    CONFIRMED: ["Tasdiqlangan", "badge-confirmed"],
    DONE: ["Bajarildi", "badge-done"],
    CANCELLED: ["Bekor qilindi", "badge-cancelled"],
  };
  const [label, cls] = map[status] || [status, ""];
  return `<span class="badge ${cls}">${label}</span>`;
}

function getInitials(name) {
  if (!name) return "?";
  return name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2);
}

function renderHeader(active) {
  const user = getUser();
  const nav = document.getElementById("header-nav");

  let html = `<a href="index.html" class="nav-link ${active === "salons" ? "btn-primary" : ""}">Salonlar</a>`;

  if (user) {
    html += `<a href="account.html" class="nav-link ${active === "account" ? "btn-primary" : ""}">Akkauntim</a>`;
    html += `<button class="btn-ghost" onclick="logout()">Chiqish</button>`;
  } else {
    html += `<a href="login.html" class="nav-link">Kirish</a>`;
    html += `<a href="register.html" class="btn-primary">Ro'yxatdan o'tish</a>`;
  }

  nav.innerHTML = html;
}

function requireAuth() {
  if (!isLoggedIn()) {
    toast("Avval tizimga kiring", "error");
    setTimeout(() => (window.location.href = "login.html"), 500);
    return false;
  }
  return true;
}

function requireCustomer() {
  if (!requireAuth()) return false;
  if (!isCustomer()) {
    toast("Faqat mijozlar uchun", "error");
    return false;
  }
  return true;
}

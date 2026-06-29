import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ---------- Chat ----------

export async function sendMessage(message, sessionId) {
  const response = await api.post("/chat", {
    message,
    session_id: sessionId,
  });
  return response.data;
}

// ---------- Orders ----------

export async function getOrderStatus(orderId) {
  const response = await api.get(`/orders/${orderId}`);
  return response.data;
}

export async function listOrders(params = {}) {
  const response = await api.get("/orders", { params });
  return response.data;
}

// ---------- Admin ----------

export async function getProducts() {
  const response = await api.get("/admin/products");
  return response.data;
}

export async function addProduct(product) {
  const response = await api.post("/admin/products", product);
  return response.data;
}

export async function updateProduct(productId, updates) {
  const response = await api.put(`/admin/products/${productId}`, updates);
  return response.data;
}

export async function deleteProduct(productId) {
  const response = await api.delete(`/admin/products/${productId}`);
  return response.data;
}

export default api;
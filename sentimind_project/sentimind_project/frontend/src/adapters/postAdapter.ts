import axios from "axios";

// Usar variable de entorno de Vite, con fallback para desarrollo
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

// Crear instancia de axios con interceptores
const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para agregar token JWT automáticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores 401 y refresh de tokens
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem("access_token", access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch {
          // Si falla el refresh, redirigir al login
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
          return Promise.reject(error);
        }
      }
    }

    return Promise.reject(error);
  }
);

// Categoría detectada con su confianza
export interface DetectedCategory {
  name: string;
  confidence: number;
}

// Información del autor
export interface Author {
  id: number;
  username: string;
}

export interface Post {
  id: number;
  content: string;
  author: Author | null; // Información del autor
  category: string; // Categoría principal (compatibilidad)
  confidence: number; // Confianza principal (compatibilidad)
  primary_category: string;
  primary_confidence: number;
  categories: DetectedCategory[]; // Múltiples categorías detectadas
  created_at: string;
}

export const postService = {
  // Obtener posts (opcionalmente filtrados por categoría)
  async getAll(category: string | null = null): Promise<Post[]> {
    const url = category
      ? `/posts/?category=${category}`
      : `/posts/`;
    const response = await api.get<Post[]>(url);
    return response.data;
  },

  // Obtener solo mis posts
  async getMine(): Promise<Post[]> {
    const response = await api.get<Post[]>(`/posts/?mine=true`);
    return response.data;
  },

  // Enviar nuevo post
  async create(content: string): Promise<Post> {
    const response = await api.post<Post>(`/posts/`, { content });
    return response.data;
  },

  // Obtener categorías disponibles
  async getCategories(): Promise<string[]> {
    const response = await api.get<{ categories: string[] }>(
      `/categories/`
    );
    return response.data.categories;
  },
};

export default api;

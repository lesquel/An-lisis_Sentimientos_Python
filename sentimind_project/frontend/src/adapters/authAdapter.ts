import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password2: string;
  first_name?: string;
  last_name?: string;
}

export interface RegisterResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}

const authApi = axios.create({
  baseURL: `${API_URL}/auth`,
});

authApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

authApi.interceptors.response.use(
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
          return authApi(originalRequest);
        } catch {
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

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const response = await authApi.post<LoginResponse>("/login/", {
      username,
      password,
    });
    return response.data;
  },

  async register(data: RegisterData): Promise<RegisterResponse> {
    const response = await authApi.post<RegisterResponse>("/register/", data);
    return response.data;
  },

  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem("refresh_token");
    try {
      await authApi.post("/logout/", { refresh: refreshToken });
    } catch {
      // Ignorar errores de logout
    }
  },

  async getProfile(): Promise<User> {
    const response = await authApi.get<User>("/me/");
    return response.data;
  },

  async requestPasswordReset(email: string): Promise<{ message: string }> {
    const response = await authApi.post<{ message: string }>("/password-reset/", {
      email,
    });
    return response.data;
  },
};

export default authApi;

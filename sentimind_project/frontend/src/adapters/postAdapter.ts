import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

export interface Post {
  id: number;
  content: string;
  category: string;
  confidence: number;
  created_at: string;
}

export const postService = {
  // Obtener posts (opcionalmente filtrados por categoría)
  async getAll(category: string | null = null): Promise<Post[]> {
    const url = category
      ? `${API_URL}/posts/?category=${category}`
      : `${API_URL}/posts/`;
    const response = await axios.get<Post[]>(url);
    return response.data;
  },

  // Enviar nuevo post
  async create(content: string): Promise<Post> {
    const response = await axios.post<Post>(`${API_URL}/posts/`, { content });
    return response.data;
  },

  // Obtener categorías disponibles
  async getCategories(): Promise<string[]> {
    const response = await axios.get<{ categories: string[] }>(
      `${API_URL}/categories/`
    );
    return response.data.categories;
  },
};

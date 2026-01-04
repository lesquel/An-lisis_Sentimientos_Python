import { useState, useEffect, useCallback } from "react";
import { postService, type Post } from "../adapters/postAdapter";

export const usePosts = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string | null>(null);

  const fetchPosts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await postService.getAll(filter);
      setPosts(data);
    } catch (err) {
      console.error("Error fetching posts", err);
      setError("Error al cargar los posts");
    } finally {
      setLoading(false);
    }
  }, [filter]);

  // Recargar cuando cambia el filtro
  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const addPost = async (content: string) => {
    setLoading(true);
    setError(null);
    try {
      await postService.create(content);
      setFilter(null); // Resetear filtro para ver el nuevo
      await fetchPosts();
    } catch (err) {
      console.error("Error creating post", err);
      setError("Error al crear el post");
    } finally {
      setLoading(false);
    }
  };

  return {
    posts,
    loading,
    error,
    filter,
    setFilter,
    addPost,
    refetch: fetchPosts,
  };
};

"use client";

import { useState, useRef, useCallback } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

async function getToken(): Promise<{ token: string; userId: string }> {
  const res = await fetch("/api/token");
  if (!res.ok) throw new Error("Failed to get token");
  return res.json();
}

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const tokenRef = useRef<{ token: string; userId: string } | null>(null);

  const ensureToken = useCallback(async () => {
    if (!tokenRef.current) {
      tokenRef.current = await getToken();
    }
    return tokenRef.current;
  }, []);

  const authFetch = useCallback(
    async (path: string, options: RequestInit = {}) => {
      const { token, userId } = await ensureToken();
      const res = await fetch(`${API_URL}/api/${userId}/tasks${path}`, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          ...options.headers,
        },
      });
      if (res.status === 401) {
        tokenRef.current = null;
        const refreshed = await ensureToken();
        const retry = await fetch(`${API_URL}/api/${refreshed.userId}/tasks${path}`, {
          ...options,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${refreshed.token}`,
            ...options.headers,
          },
        });
        return retry;
      }
      return res;
    },
    [ensureToken]
  );

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await authFetch("/");
      if (!res.ok) throw new Error("Failed to fetch tasks");
      setTasks(await res.json());
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
  }, [authFetch]);

  const createTask = useCallback(
    async (title: string, description?: string) => {
      const res = await authFetch("/", {
        method: "POST",
        body: JSON.stringify({ title, description: description || null }),
      });
      if (!res.ok) throw new Error("Failed to create task");
      const task = await res.json();
      setTasks((prev) => [...prev, task]);
      return task;
    },
    [authFetch]
  );

  const updateTask = useCallback(
    async (id: number, data: { title?: string; description?: string | null }) => {
      const res = await authFetch(`/${id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("Failed to update task");
      const updated = await res.json();
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
      return updated;
    },
    [authFetch]
  );

  const deleteTask = useCallback(
    async (id: number) => {
      const res = await authFetch(`/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Failed to delete task");
      setTasks((prev) => prev.filter((t) => t.id !== id));
    },
    [authFetch]
  );

  const toggleComplete = useCallback(
    async (id: number) => {
      const res = await authFetch(`/${id}/complete`, { method: "PATCH" });
      if (!res.ok) throw new Error("Failed to toggle task");
      const updated = await res.json();
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
      return updated;
    },
    [authFetch]
  );

  return { tasks, loading, error, fetchTasks, createTask, updateTask, deleteTask, toggleComplete };
}

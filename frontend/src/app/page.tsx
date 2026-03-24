"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { useTasks } from "@/hooks/useTasks";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";

export default function Dashboard() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const { tasks, loading, error, fetchTasks, createTask, updateTask, deleteTask, toggleComplete } = useTasks();

  useEffect(() => {
    if (!isPending && session) {
      fetchTasks();
    }
  }, [isPending, session, fetchTasks]);

  const handleSignOut = async () => {
    await signOut();
    router.push("/auth/signin");
  };

  if (isPending) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          <p className="text-sm text-gray-500">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-sm font-bold text-white">
              T
            </div>
            <div>
              <h1 className="text-base font-bold text-gray-900">Todo App</h1>
              <p className="text-xs text-gray-500">{session.user.email}</p>
            </div>
          </div>
          <button
            onClick={handleSignOut}
            className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-50 hover:text-gray-900"
          >
            Sign Out
          </button>
        </div>
      </header>
      <main className="mx-auto max-w-2xl space-y-6 px-4 py-8">
        <TaskForm onSubmit={createTask} />
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}
        <TaskList
          tasks={tasks}
          loading={loading}
          onToggle={toggleComplete}
          onDelete={deleteTask}
          onUpdate={updateTask}
        />
      </main>
    </div>
  );
}

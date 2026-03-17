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
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-4">
          <div>
            <h1 className="text-lg font-bold text-gray-900">Todo App</h1>
            <p className="text-sm text-gray-500">{session.user.email}</p>
          </div>
          <button
            onClick={handleSignOut}
            className="rounded-md bg-gray-100 px-3 py-1.5 text-sm text-gray-700 hover:bg-gray-200"
          >
            Sign Out
          </button>
        </div>
      </header>
      <main className="mx-auto max-w-2xl space-y-6 px-4 py-6">
        <TaskForm onSubmit={createTask} />
        {error && <p className="text-sm text-red-600">{error}</p>}
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

"use client";

import TaskCard from "./TaskCard";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
}

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onUpdate: (id: number, data: { title?: string; description?: string }) => Promise<void>;
}

export default function TaskList({ tasks, loading, onToggle, onDelete, onUpdate }: TaskListProps) {
  if (loading) {
    return <p className="py-8 text-center text-sm text-gray-500">Loading tasks...</p>;
  }

  if (tasks.length === 0) {
    return <p className="py-8 text-center text-sm text-gray-500">No tasks yet. Add one above!</p>;
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onToggle={onToggle} onDelete={onDelete} onUpdate={onUpdate} />
      ))}
    </div>
  );
}

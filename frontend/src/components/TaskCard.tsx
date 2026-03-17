"use client";

import { useState } from "react";

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
}

interface TaskCardProps {
  task: Task;
  onToggle: (id: number) => Promise<void>;
  onDelete: (id: number) => Promise<void>;
  onUpdate: (id: number, data: { title?: string; description?: string }) => Promise<void>;
}

export default function TaskCard({ task, onToggle, onDelete, onUpdate }: TaskCardProps) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [busy, setBusy] = useState(false);

  const handleSave = async () => {
    if (!title.trim()) return;
    setBusy(true);
    try {
      await onUpdate(task.id, { title: title.trim(), description: description.trim() || undefined });
      setEditing(false);
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    setBusy(true);
    try {
      await onDelete(task.id);
    } finally {
      setBusy(false);
    }
  };

  const handleToggle = async () => {
    setBusy(true);
    try {
      await onToggle(task.id);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className={`rounded-lg border bg-white p-4 shadow-sm ${task.completed ? "border-green-200 bg-green-50" : "border-gray-200"}`}>
      {editing ? (
        <div className="space-y-2">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:border-blue-500 focus:outline-none"
            maxLength={200}
          />
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:border-blue-500 focus:outline-none"
            maxLength={1000}
          />
          <div className="flex gap-2">
            <button onClick={handleSave} disabled={busy} className="rounded bg-blue-600 px-3 py-1 text-xs text-white hover:bg-blue-700 disabled:opacity-50">
              Save
            </button>
            <button onClick={() => { setEditing(false); setTitle(task.title); setDescription(task.description || ""); }} className="rounded bg-gray-200 px-3 py-1 text-xs hover:bg-gray-300">
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <h3 className={`font-medium ${task.completed ? "line-through text-gray-500" : "text-gray-900"}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? "text-gray-400" : "text-gray-600"}`}>
                {task.description}
              </p>
            )}
          </div>
          <div className="flex gap-1 shrink-0">
            <button onClick={handleToggle} disabled={busy} className={`rounded px-2 py-1 text-xs font-medium ${task.completed ? "bg-yellow-100 text-yellow-700 hover:bg-yellow-200" : "bg-green-100 text-green-700 hover:bg-green-200"} disabled:opacity-50`}>
              {task.completed ? "Undo" : "Done"}
            </button>
            <button onClick={() => setEditing(true)} disabled={busy} className="rounded bg-gray-100 px-2 py-1 text-xs text-gray-700 hover:bg-gray-200 disabled:opacity-50">
              Edit
            </button>
            <button onClick={handleDelete} disabled={busy} className="rounded bg-red-100 px-2 py-1 text-xs text-red-700 hover:bg-red-200 disabled:opacity-50">
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

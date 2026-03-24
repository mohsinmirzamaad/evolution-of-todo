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
  onUpdate: (id: number, data: { title?: string; description?: string | null }) => Promise<void>;
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
      await onUpdate(task.id, { title: title.trim(), description: description.trim() || null });
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
    <div className={`rounded-xl border bg-white p-4 shadow-sm transition-colors ${task.completed ? "border-green-200 bg-green-50/50" : "border-gray-200"}`}>
      {editing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            maxLength={200}
          />
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            maxLength={1000}
          />
          <div className="flex gap-2">
            <button onClick={handleSave} disabled={busy} className="rounded-lg bg-blue-600 px-3.5 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-blue-700 disabled:opacity-50">
              Save
            </button>
            <button onClick={() => { setEditing(false); setTitle(task.title); setDescription(task.description || ""); }} className="rounded-lg border border-gray-200 bg-white px-3.5 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-gray-50">
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0 flex-1">
            <h3 className={`font-medium ${task.completed ? "text-gray-400 line-through" : "text-gray-900"}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? "text-gray-400" : "text-gray-500"}`}>
                {task.description}
              </p>
            )}
          </div>
          <div className="flex gap-1.5 shrink-0">
            <button onClick={handleToggle} disabled={busy} className={`rounded-lg px-2.5 py-1.5 text-xs font-medium transition-colors ${task.completed ? "bg-amber-50 text-amber-700 hover:bg-amber-100" : "bg-green-50 text-green-700 hover:bg-green-100"} disabled:opacity-50`}>
              {task.completed ? "Undo" : "Done"}
            </button>
            <button onClick={() => setEditing(true)} disabled={busy} className="rounded-lg border border-gray-200 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-gray-50 disabled:opacity-50">
              Edit
            </button>
            <button onClick={handleDelete} disabled={busy} className="rounded-lg bg-red-50 px-2.5 py-1.5 text-xs font-medium text-red-600 transition-colors hover:bg-red-100 disabled:opacity-50">
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { useSession } from "@/lib/auth-client";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function getToken(): Promise<{ token: string; userId: string }> {
  const res = await fetch("/api/token");
  if (!res.ok) throw new Error("Failed to get token");
  return res.json();
}

export default function ChatPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();
  const [token, setToken] = useState<string | null>(null);
  const tokenRef = useRef<string | null>(null);

  useEffect(() => {
    if (!isPending && session) {
      getToken().then(({ token }) => {
        tokenRef.current = token;
        setToken(token);
      });
    }
  }, [isPending, session]);

  const { control } = useChatKit({
    api: {
      url: `${API_URL}/chatkit`,
      domainKey: "local-dev",
      fetch: (input, init) => {
        const headers = new Headers(init?.headers);
        if (tokenRef.current) {
          headers.set("Authorization", `Bearer ${tokenRef.current}`);
        }
        return fetch(input, { ...init, headers });
      },
    },
    startScreen: {
      greeting: "Hi! I can help you manage your todos. Try saying things like:",
      prompts: [
        { label: "Add a task", prompt: "Add a task called Buy groceries" },
        { label: "Show my tasks", prompt: "Show all my tasks" },
        { label: "Complete a task", prompt: "Mark my first task as done" },
      ],
    },
    composer: {
      placeholder: "Ask me to manage your todos...",
    },
    history: {
      enabled: true,
      showDelete: true,
    },
  });

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

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
          <p className="text-sm text-gray-500">Connecting to AI...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-gray-50">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 text-sm font-bold text-white">
              T
            </div>
            <div>
              <h1 className="text-base font-bold text-gray-900">AI Chat</h1>
              <p className="text-xs text-gray-500">{session.user.email}</p>
            </div>
          </div>
          <button
            onClick={() => router.push("/")}
            className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-50 hover:text-gray-900"
          >
            Back to Tasks
          </button>
        </div>
      </header>
      <main className="flex flex-1 justify-center">
        <div className="w-full max-w-4xl flex-1">
          <ChatKit control={control} className="h-[calc(100vh-73px)] w-full" />
        </div>
      </main>
    </div>
  );
}

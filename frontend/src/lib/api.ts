/**
 * API client for S1NGULARITY backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
  timestamp?: string;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  task_type?: string;
  context?: Record<string, any>;
}

export interface ChatResponse {
  session_id: string;
  message: string;
  task_type?: string;
  modules_loaded?: string[];
  sources?: Array<{ title: string; url: string }>;
  metadata?: Record<string, any>;
}

export interface FeedbackRequest {
  session_id: string;
  feedback_type: "hallucination" | "bias" | "error" | "suggestion";
  message: string;
  context?: Record<string, any>;
  severity?: "info" | "warning" | "error" | "critical";
}

export interface HealthResponse {
  status: string;
  version: string;
  services: {
    database: boolean;
    jobdiva: boolean;
    llm: boolean;
    web_search: boolean;
  };
}

/**
 * Send a chat message to the S1NGULARITY API
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `API request failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Submit user feedback
 */
export async function submitFeedback(
  request: FeedbackRequest
): Promise<{ status: string; message: string }> {
  const response = await fetch(`${API_URL}/feedback`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Feedback submission failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Upload a PDF resume
 */
export async function uploadResume(file: File): Promise<{ text: string }> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload-resume`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Resume upload failed: ${response.statusText}`);
  }

  return response.json();
}

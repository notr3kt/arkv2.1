export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  taskType?: string;
  modulesLoaded?: string[];
  sources?: Source[];
  metadata?: Record<string, any>;
}

export interface Source {
  title: string;
  url: string;
  content?: string;
}

export interface CandidateAnalysis {
  matchScore?: number;
  skillMatch?: number;
  experienceMatch?: number;
  greenFlags?: string[];
  yellowFlags?: string[];
  redFlags?: string[];
  biasFlags?: string[];
  recommendation?: string;
}

export interface Session {
  id: string;
  createdAt: string;
  lastActive: string;
  messageCount: number;
  taskType?: string;
}

export type TaskType =
  | "jd_analysis"
  | "resume_screening"
  | "boolean_search"
  | "salary_research"
  | "bias_check"
  | "candidate_outreach"
  | "analytics"
  | "general";

export interface ActionButton {
  id: string;
  label: string;
  icon: React.ReactNode;
  taskType: TaskType;
  prompt: string;
  requiresContext?: boolean;
}

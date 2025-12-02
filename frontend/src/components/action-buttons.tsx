"use client";

import {
  FileText,
  Search,
  DollarSign,
  Mail,
  AlertCircle,
  Briefcase,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TaskType } from "@/types";

interface ActionButtonsProps {
  onActionClick: (taskType: TaskType, prompt: string) => void;
  hasContext?: boolean;
}

const ACTIONS = [
  {
    id: "jd-analysis",
    label: "Analyze Job",
    icon: <Briefcase className="h-4 w-4" />,
    taskType: "jd_analysis" as TaskType,
    prompt: "Analyze this job description and provide a detailed breakdown.",
    color: "bg-blue-500",
  },
  {
    id: "resume-screen",
    label: "Screen Resume",
    icon: <FileText className="h-4 w-4" />,
    taskType: "resume_screening" as TaskType,
    prompt: "Screen this candidate's resume and provide a match score.",
    color: "bg-green-500",
    requiresContext: true,
  },
  {
    id: "boolean-search",
    label: "Boolean Query",
    icon: <Search className="h-4 w-4" />,
    taskType: "boolean_search" as TaskType,
    prompt: "Generate a boolean search query for this role.",
    color: "bg-purple-500",
  },
  {
    id: "salary-research",
    label: "Salary Data",
    icon: <DollarSign className="h-4 w-4" />,
    taskType: "salary_research" as TaskType,
    prompt: "What is the market salary range for this position?",
    color: "bg-yellow-500",
  },
  {
    id: "outreach",
    label: "Draft Email",
    icon: <Mail className="h-4 w-4" />,
    taskType: "candidate_outreach" as TaskType,
    prompt: "Draft an outreach email for this candidate.",
    color: "bg-pink-500",
    requiresContext: true,
  },
  {
    id: "bias-check",
    label: "Bias Check",
    icon: <AlertCircle className="h-4 w-4" />,
    taskType: "bias_check" as TaskType,
    prompt: "Check this job description for potential bias.",
    color: "bg-red-500",
  },
];

export function ActionButtons({ onActionClick, hasContext }: ActionButtonsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Quick Actions</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2">
          {ACTIONS.map((action) => (
            <Button
              key={action.id}
              variant="outline"
              className="justify-start gap-2 h-auto py-3"
              onClick={() => onActionClick(action.taskType, action.prompt)}
              disabled={action.requiresContext && !hasContext}
            >
              <div className={`p-1.5 rounded ${action.color} text-white`}>
                {action.icon}
              </div>
              <span className="text-sm">{action.label}</span>
            </Button>
          ))}
        </div>

        {!hasContext && (
          <p className="text-xs text-muted-foreground mt-4 text-center">
            Upload a resume to enable context-specific actions
          </p>
        )}
      </CardContent>
    </Card>
  );
}

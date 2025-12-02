"use client";

import { useState, useEffect } from "react";
import { Sparkles, Activity } from "lucide-react";
import { ChatInterface } from "@/components/chat-interface";
import { PDFUpload } from "@/components/pdf-upload";
import { ActionButtons } from "@/components/action-buttons";
import { AnalysisSidebar } from "@/components/analysis-sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { checkHealth } from "@/lib/api";
import { CandidateAnalysis, TaskType } from "@/types";

export default function Home() {
  const [sessionId] = useState(() => `session-${Date.now()}`);
  const [uploadedResume, setUploadedResume] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<CandidateAnalysis | null>(null);
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);

  // Check backend health on mount
  useEffect(() => {
    checkHealth()
      .then(() => setIsBackendHealthy(true))
      .catch(() => setIsBackendHealthy(false));
  }, []);

  const handleUploadComplete = (text: string, file: File) => {
    setUploadedResume(text);
    setCurrentFile(file);
  };

  const handleAnalysisUpdate = (metadata: any) => {
    if (metadata.analysis) {
      setAnalysis(metadata.analysis);
    }
  };

  const handleActionClick = (taskType: TaskType, prompt: string) => {
    // This would trigger the chat to send the prompt
    // For now, we'll just log it
    console.log("Action clicked:", taskType, prompt);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary rounded-lg">
                <Sparkles className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight">
                  S1NGULARITY
                </h1>
                <p className="text-sm text-muted-foreground">
                  AI-Powered Recruiting Intelligence
                </p>
              </div>
            </div>

            {/* Health indicator */}
            <div className="flex items-center gap-2">
              <Activity
                className={`h-4 w-4 ${
                  isBackendHealthy === null
                    ? "text-yellow-500"
                    : isBackendHealthy
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              />
              <span className="text-sm text-muted-foreground">
                {isBackendHealthy === null
                  ? "Checking..."
                  : isBackendHealthy
                  ? "Connected"
                  : "Disconnected"}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 container mx-auto px-4 py-6 overflow-hidden">
        <div className="h-full grid grid-cols-12 gap-6">
          {/* Left Sidebar - PDF Upload & Actions */}
          <div className="col-span-3 space-y-4 overflow-y-auto">
            <PDFUpload
              onUploadComplete={handleUploadComplete}
              onError={(error) => console.error(error)}
            />

            <ActionButtons
              onActionClick={handleActionClick}
              hasContext={!!uploadedResume}
            />

            {currentFile && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm">Current Resume</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm">
                    <p className="font-medium truncate">{currentFile.name}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      {(currentFile.size / 1024).toFixed(2)} KB
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Center - Chat Interface */}
          <div className="col-span-6 h-full">
            <Card className="h-full flex flex-col">
              <ChatInterface
                sessionId={sessionId}
                onAnalysisUpdate={handleAnalysisUpdate}
                context={
                  uploadedResume
                    ? {
                        resume_text: uploadedResume,
                        resume_file_name: currentFile?.name,
                      }
                    : undefined
                }
              />
            </Card>
          </div>

          {/* Right Sidebar - Analysis */}
          <div className="col-span-3 h-full overflow-y-auto">
            <AnalysisSidebar analysis={analysis} />
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t bg-card py-3">
        <div className="container mx-auto px-4">
          <p className="text-xs text-center text-muted-foreground">
            S1NGULARITY v1.0 • Powered by AI • Evidence-Based Recruiting
          </p>
        </div>
      </footer>
    </div>
  );
}

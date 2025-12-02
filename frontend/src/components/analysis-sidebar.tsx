"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CandidateAnalysis } from "@/types";
import { CheckCircle2, AlertTriangle, XCircle, AlertCircle } from "lucide-react";

interface AnalysisSidebarProps {
  analysis: CandidateAnalysis | null;
}

export function AnalysisSidebar({ analysis }: AnalysisSidebarProps) {
  if (!analysis) {
    return (
      <Card className="h-full">
        <CardHeader>
          <CardTitle className="text-lg">Candidate Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground text-center py-8">
            Upload a resume and ask for analysis to see results here
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="text-lg">Candidate Analysis</CardTitle>
      </CardHeader>
      <CardContent className="flex-1 overflow-hidden">
        <ScrollArea className="h-full">
          <div className="space-y-6">
            {/* Match Score */}
            {analysis.matchScore !== undefined && (
              <div>
                <h3 className="font-semibold text-sm mb-2">Overall Match</h3>
                <div className="relative">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-2xl font-bold text-primary">
                      {analysis.matchScore}%
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {analysis.matchScore >= 80
                        ? "Excellent"
                        : analysis.matchScore >= 60
                        ? "Good"
                        : analysis.matchScore >= 40
                        ? "Fair"
                        : "Poor"}
                    </span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary transition-all"
                      style={{ width: `${analysis.matchScore}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Skill Match */}
            {analysis.skillMatch !== undefined && (
              <div>
                <h3 className="font-semibold text-sm mb-2">Skill Match</h3>
                <div className="flex items-center justify-between">
                  <span className="text-xl font-semibold">{analysis.skillMatch}%</span>
                  <div className="h-2 flex-1 mx-3 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500"
                      style={{ width: `${analysis.skillMatch}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Experience Match */}
            {analysis.experienceMatch !== undefined && (
              <div>
                <h3 className="font-semibold text-sm mb-2">Experience Match</h3>
                <div className="flex items-center justify-between">
                  <span className="text-xl font-semibold">{analysis.experienceMatch}%</span>
                  <div className="h-2 flex-1 mx-3 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500"
                      style={{ width: `${analysis.experienceMatch}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Green Flags */}
            {analysis.greenFlags && analysis.greenFlags.length > 0 && (
              <div>
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-green-500" />
                  Green Flags
                </h3>
                <ul className="space-y-1">
                  {analysis.greenFlags.map((flag, idx) => (
                    <li key={idx} className="text-sm flex items-start gap-2">
                      <span className="text-green-500">•</span>
                      <span>{flag}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Yellow Flags */}
            {analysis.yellowFlags && analysis.yellowFlags.length > 0 && (
              <div>
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-500" />
                  Yellow Flags
                </h3>
                <ul className="space-y-1">
                  {analysis.yellowFlags.map((flag, idx) => (
                    <li key={idx} className="text-sm flex items-start gap-2">
                      <span className="text-yellow-500">•</span>
                      <span>{flag}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Red Flags */}
            {analysis.redFlags && analysis.redFlags.length > 0 && (
              <div>
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2">
                  <XCircle className="h-4 w-4 text-red-500" />
                  Red Flags
                </h3>
                <ul className="space-y-1">
                  {analysis.redFlags.map((flag, idx) => (
                    <li key={idx} className="text-sm flex items-start gap-2">
                      <span className="text-red-500">•</span>
                      <span>{flag}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Bias Flags */}
            {analysis.biasFlags && analysis.biasFlags.length > 0 && (
              <div className="p-3 bg-red-50 dark:bg-red-950 rounded-lg border border-red-200 dark:border-red-800">
                <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-red-700 dark:text-red-300">
                  <AlertCircle className="h-4 w-4" />
                  Bias Detected
                </h3>
                <ul className="space-y-1">
                  {analysis.biasFlags.map((flag, idx) => (
                    <li key={idx} className="text-sm text-red-700 dark:text-red-300">
                      • {flag}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendation */}
            {analysis.recommendation && (
              <div className="pt-4 border-t">
                <h3 className="font-semibold text-sm mb-2">Recommendation</h3>
                <p className="text-sm text-muted-foreground">
                  {analysis.recommendation}
                </p>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}

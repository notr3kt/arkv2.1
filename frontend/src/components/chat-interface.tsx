"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { sendChatMessage } from "@/lib/api";
import { Message, TaskType } from "@/types";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

interface ChatInterfaceProps {
  sessionId: string;
  onAnalysisUpdate?: (analysis: any) => void;
  context?: Record<string, any>;
}

export function ChatInterface({
  sessionId,
  onAnalysisUpdate,
  context,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentTaskType, setCurrentTaskType] = useState<TaskType | undefined>();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendChatMessage({
        message: input,
        session_id: sessionId,
        task_type: currentTaskType,
        context,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message,
        timestamp: new Date().toISOString(),
        taskType: response.task_type,
        modulesLoaded: response.modules_loaded,
        sources: response.sources,
        metadata: response.metadata,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Update task type if changed
      if (response.task_type) {
        setCurrentTaskType(response.task_type as TaskType);
      }

      // Notify parent of analysis updates
      if (response.metadata && onAnalysisUpdate) {
        onAnalysisUpdate(response.metadata);
      }
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `Sorry, I encountered an error: ${
          error instanceof Error ? error.message : "Unknown error"
        }`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef as any}>
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-muted-foreground py-12">
              <h3 className="text-lg font-semibold mb-2">
                Welcome to S1NGULARITY
              </h3>
              <p className="text-sm">
                Your AI-powered recruiting assistant. Ask me anything about:
              </p>
              <ul className="text-sm mt-2 space-y-1">
                <li>• Job description analysis</li>
                <li>• Resume screening</li>
                <li>• Salary research</li>
                <li>• Boolean search queries</li>
                <li>• Candidate outreach</li>
              </ul>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex",
                message.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <Card
                className={cn(
                  "max-w-[80%] p-4",
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                )}
              >
                <div className="prose prose-sm max-w-none dark:prose-invert">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                {/* Show metadata for assistant messages */}
                {message.role === "assistant" && message.modulesLoaded && (
                  <div className="mt-3 pt-3 border-t border-border/40 text-xs text-muted-foreground">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold">Modules:</span>
                      <span>{message.modulesLoaded.join(", ")}</span>
                    </div>
                    {message.taskType && (
                      <div className="flex items-center gap-2 mt-1">
                        <span className="font-semibold">Task:</span>
                        <span className="capitalize">
                          {message.taskType.replace("_", " ")}
                        </span>
                      </div>
                    )}
                  </div>
                )}

                {/* Show sources if available */}
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-border/40">
                    <p className="text-xs font-semibold mb-2">Sources:</p>
                    <ul className="text-xs space-y-1">
                      {message.sources.map((source, idx) => (
                        <li key={idx}>
                          <a
                            href={source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:underline"
                          >
                            {source.title}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                <div className="text-xs text-muted-foreground mt-2">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </Card>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <Card className="bg-muted p-4">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm text-muted-foreground">
                    Thinking...
                  </span>
                </div>
              </Card>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="border-t p-4">
        <div className="flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            size="icon"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>

        {/* Task type indicator */}
        {currentTaskType && (
          <div className="mt-2 text-xs text-muted-foreground">
            Current mode: <span className="capitalize font-semibold">{currentTaskType.replace("_", " ")}</span>
          </div>
        )}
      </div>
    </div>
  );
}

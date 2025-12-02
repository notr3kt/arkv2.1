"""S1NGULARITY FastAPI Application.

Main application orchestrating:
- LangGraph agent with intelligent module loading
- JobDiva integration
- Web search capabilities
- Feedback logging
"""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

# Import our custom modules
from database import (
    get_db_session,
    init_db,
    FeedbackLog,
    SessionHistory,
    CandidateInteraction,
)
from module_loader import ModuleLoader, TaskType, get_module_loader
from web_search_tool import WebSearchTool, get_web_search_tool
from jobdiva_client import JobDivaClient, SearchCandidateRequest, CreateCandidateRequest
from jobdiva_auth import get_auth


# ==============================================
# REQUEST/RESPONSE MODELS
# ==============================================

class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ChatRequest(BaseModel):
    """Chat request from user."""
    message: str = Field(..., description="User message", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    task_type: Optional[str] = Field(None, description="Task type hint: jd_analysis, resume_screening, etc.")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context (job_id, candidate_id, etc.)")


class ChatResponse(BaseModel):
    """Chat response from S1NGULARITY."""
    session_id: str
    message: str
    task_type: Optional[str] = None
    modules_loaded: List[str] = Field(default_factory=list)
    sources: Optional[List[Dict[str, str]]] = None  # Web search sources
    metadata: Optional[Dict[str, Any]] = None


class FeedbackRequest(BaseModel):
    """User feedback submission."""
    session_id: str
    feedback_type: str = Field(..., description="Type: hallucination, bias, error, suggestion")
    message: str
    context: Optional[Dict[str, Any]] = None
    severity: str = Field(default="info", description="Severity: info, warning, error, critical")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    services: Dict[str, bool]


# ==============================================
# APPLICATION LIFECYCLE
# ==============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    # Startup
    print("🚀 Starting S1NGULARITY...")
    await init_db()
    print("✅ Database initialized")

    yield

    # Shutdown
    print("👋 Shutting down S1NGULARITY...")


# ==============================================
# FASTAPI APP
# ==============================================

app = FastAPI(
    title="S1NGULARITY API",
    description="AI-Powered Recruiting Intelligence Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================
# AGENT ORCHESTRATION (Simplified - LangGraph would go here)
# ==============================================

class S1NGULARITYAgent:
    """Main agent orchestrating JobDiva, Web Search, and Module Loading.

    NOTE: This is a simplified version. Full LangGraph implementation would include:
    - State management
    - Multi-step reasoning
    - Tool calling loops
    - Memory persistence
    """

    def __init__(
        self,
        module_loader: ModuleLoader,
        web_search: WebSearchTool,
        jobdiva_client: JobDivaClient,
        llm_provider: str = "anthropic"
    ):
        self.module_loader = module_loader
        self.web_search = web_search
        self.jobdiva = jobdiva_client
        self.llm_provider = llm_provider

        # Initialize LLM (Anthropic or OpenAI)
        if llm_provider == "anthropic":
            try:
                from anthropic import AsyncAnthropic
                self.llm = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20250101")
            except ImportError:
                raise RuntimeError("anthropic package not installed")
        elif llm_provider == "openai":
            try:
                from openai import AsyncOpenAI
                self.llm = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
            except ImportError:
                raise RuntimeError("openai package not installed")
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    def detect_task_type(self, message: str) -> TaskType:
        """Detect task type from user message."""
        message_lower = message.lower()

        if any(kw in message_lower for kw in ["job description", "jd", "analyze role", "break down"]):
            return TaskType.JD_ANALYSIS
        elif any(kw in message_lower for kw in ["resume", "cv", "candidate", "screen"]):
            return TaskType.RESUME_SCREENING
        elif any(kw in message_lower for kw in ["boolean", "search string", "query"]):
            return TaskType.BOOLEAN_SEARCH
        elif any(kw in message_lower for kw in ["salary", "market rate", "compensation"]):
            return TaskType.SALARY_RESEARCH
        elif any(kw in message_lower for kw in ["bias", "fairness", "diversity"]):
            return TaskType.BIAS_CHECK
        elif any(kw in message_lower for kw in ["outreach", "email", "message", "contact"]):
            return TaskType.CANDIDATE_OUTREACH
        elif any(kw in message_lower for kw in ["analytics", "metrics", "dashboard"]):
            return TaskType.ANALYTICS
        else:
            return TaskType.GENERAL

    async def process_message(
        self,
        message: str,
        session_id: str,
        task_type: Optional[TaskType] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process user message and generate response.

        This is a simplified implementation. Full version would use LangGraph
        for multi-step reasoning and tool calling.
        """
        # 1. Detect task type if not provided
        if task_type is None:
            task_type = self.detect_task_type(message)

        # 2. Load relevant modules
        system_prompt = self.module_loader.build_system_prompt(
            task_type=task_type,
            include_master=True,
            include_modules=True
        )

        modules_loaded = [
            m.name for m in self.module_loader.load_modules_for_task(task_type)
        ]

        # 3. Prepare tools context
        tools_available = []
        if task_type == TaskType.SALARY_RESEARCH:
            tools_available.append("web_search_salary")
        if task_type in [TaskType.RESUME_SCREENING, TaskType.JD_ANALYSIS]:
            tools_available.append("search_jobdiva_candidates")

        tools_context = f"\n\n# AVAILABLE TOOLS\n{', '.join(tools_available)}" if tools_available else ""

        # 4. Call LLM
        if self.llm_provider == "anthropic":
            response = await self._call_anthropic(
                system_prompt + tools_context,
                message,
                context
            )
        else:
            response = await self._call_openai(
                system_prompt + tools_context,
                message,
                context
            )

        return {
            "response": response,
            "task_type": task_type.value,
            "modules_loaded": modules_loaded,
        }

    async def _call_anthropic(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Call Anthropic API."""
        messages = [{"role": "user", "content": user_message}]

        if context:
            context_str = f"\n\nContext: {context}"
            messages[0]["content"] += context_str

        response = await self.llm.messages.create(
            model=self.model,
            max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "4096")),
            temperature=float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7")),
            system=system_prompt,
            messages=messages
        )

        return response.content[0].text

    async def _call_openai(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Call OpenAI API."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})

        response = await self.llm.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "4096")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        )

        return response.choices[0].message.content


# ==============================================
# DEPENDENCY INJECTION
# ==============================================

def get_agent() -> S1NGULARITYAgent:
    """Get S1NGULARITY agent instance."""
    return S1NGULARITYAgent(
        module_loader=get_module_loader(),
        web_search=get_web_search_tool(),
        jobdiva_client=JobDivaClient(auth=get_auth()),
        llm_provider=os.getenv("LLM_PROVIDER", "anthropic")
    )


# ==============================================
# API ENDPOINTS
# ==============================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with health check."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": True,
            "jobdiva": bool(os.getenv("JOBDIVA_CLIENT_ID")),
            "llm": bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")),
            "web_search": bool(os.getenv("TAVILY_API_KEY")),
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return await root()


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    agent: S1NGULARITYAgent = Depends(get_agent)
):
    """Main chat endpoint for S1NGULARITY interactions."""
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # Detect or use provided task type
    task_type = None
    if request.task_type:
        try:
            task_type = TaskType(request.task_type)
        except ValueError:
            pass

    # Process message with agent
    try:
        result = await agent.process_message(
            message=request.message,
            session_id=session_id,
            task_type=task_type,
            context=request.context
        )

        # Update session history in background
        background_tasks.add_task(
            update_session_history,
            db=db,
            session_id=session_id,
            task_type=result["task_type"]
        )

        return ChatResponse(
            session_id=session_id,
            message=result["response"],
            task_type=result["task_type"],
            modules_loaded=result["modules_loaded"],
            metadata={"context": request.context}
        )

    except Exception as e:
        # Log error
        background_tasks.add_task(
            log_error,
            db=db,
            session_id=session_id,
            error=str(e),
            context={"message": request.message}
        )
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")


@app.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """Submit user feedback for continuous improvement."""
    feedback_log = FeedbackLog(
        session_id=request.session_id,
        error_type=request.feedback_type,
        category="user_feedback",
        severity=request.severity,
        user_input=request.message,
        context=request.context,
        resolved=False
    )

    db.add(feedback_log)
    await db.commit()

    return {"status": "success", "message": "Feedback recorded. Thank you!"}


@app.post("/jobdiva/search-candidates")
async def search_candidates(
    request: SearchCandidateRequest,
    jobdiva_client: JobDivaClient = Depends(lambda: JobDivaClient(auth=get_auth()))
):
    """Direct JobDiva candidate search endpoint."""
    try:
        results = jobdiva_client.search_candidate_profile(request)
        return {"candidates": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JobDiva search failed: {str(e)}")


# ==============================================
# BACKGROUND TASKS
# ==============================================

async def update_session_history(db: AsyncSession, session_id: str, task_type: str):
    """Update session history in database."""
    # Check if session exists
    from sqlalchemy import select
    stmt = select(SessionHistory).where(SessionHistory.session_id == session_id)
    result = await db.execute(stmt)
    session = result.scalar_one_or_none()

    if session:
        session.last_active = datetime.utcnow()
        session.message_count += 1
        session.task_type = task_type
    else:
        session = SessionHistory(
            session_id=session_id,
            task_type=task_type,
            message_count=1
        )
        db.add(session)

    await db.commit()


async def log_error(db: AsyncSession, session_id: str, error: str, context: Dict[str, Any]):
    """Log error to database."""
    error_log = FeedbackLog(
        session_id=session_id,
        error_type="technical_error",
        category="system",
        severity="error",
        context=context,
        system_response=error
    )
    db.add(error_log)
    await db.commit()


# ==============================================
# MAIN ENTRY POINT
# ==============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() == "true",
        workers=int(os.getenv("WORKERS", "1"))
    )

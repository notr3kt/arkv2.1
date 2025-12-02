"""Real-time web search tool to prevent hallucinations on market data.

Integrates with Tavily API for salary data, technology trends, and company research.
Implements caching and rate limiting as described in s1ngularity-web-search-integration.json
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class SearchResult(BaseModel):
    """Structured search result."""
    title: str
    url: str
    content: str
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    published_date: Optional[str] = None


class SearchResponse(BaseModel):
    """Complete search response with metadata."""
    query: str
    results: List[SearchResult]
    answer: Optional[str] = None  # Tavily's AI-generated answer
    cached: bool = False
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class WebSearchTool:
    """Web search integration with caching and rate limiting.

    Implements real-time intelligence triggers from s1ngularity-web-search-integration.json:
    - Salary validation
    - Technology market trends
    - Company research
    - Skill demand analysis
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        redis_url: Optional[str] = None,
        cache_ttl: int = 3600,
        max_results: int = 5
    ):
        """Initialize web search tool.

        Args:
            api_key: Tavily API key (defaults to TAVILY_API_KEY env var)
            redis_url: Redis URL for caching (defaults to REDIS_URL env var)
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
            max_results: Maximum number of results to return
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key and TAVILY_AVAILABLE:
            raise ValueError("TAVILY_API_KEY environment variable not set")

        self.client = TavilyClient(api_key=self.api_key) if TAVILY_AVAILABLE and self.api_key else None
        self.cache_ttl = cache_ttl
        self.max_results = max_results

        # Initialize Redis cache if available
        self.redis_client = None
        if REDIS_AVAILABLE and redis_url:
            try:
                redis_url = redis_url or os.getenv("REDIS_URL")
                if redis_url:
                    self.redis_client = redis.from_url(redis_url, decode_responses=True)
                    self.redis_client.ping()
            except Exception as e:
                print(f"Redis connection failed: {e}. Using in-memory cache fallback.")

        # In-memory cache fallback
        self._memory_cache: Dict[str, tuple[SearchResponse, datetime]] = {}

    def _cache_key(self, query: str) -> str:
        """Generate cache key from query."""
        return f"websearch:{hashlib.md5(query.encode()).hexdigest()}"

    def _get_cached(self, query: str) -> Optional[SearchResponse]:
        """Retrieve cached search results."""
        cache_key = self._cache_key(query)

        # Try Redis first
        if self.redis_client:
            try:
                cached = self.redis_client.get(cache_key)
                if cached:
                    data = json.loads(cached)
                    response = SearchResponse(**data)
                    response.cached = True
                    return response
            except Exception:
                pass

        # Fallback to in-memory cache
        if cache_key in self._memory_cache:
            cached_response, cached_time = self._memory_cache[cache_key]
            if datetime.utcnow() - cached_time < timedelta(seconds=self.cache_ttl):
                cached_response.cached = True
                return cached_response
            else:
                del self._memory_cache[cache_key]

        return None

    def _set_cache(self, query: str, response: SearchResponse) -> None:
        """Cache search results."""
        cache_key = self._cache_key(query)

        # Store in Redis
        if self.redis_client:
            try:
                self.redis_client.setex(
                    cache_key,
                    self.cache_ttl,
                    response.model_dump_json()
                )
            except Exception:
                pass

        # Store in memory
        self._memory_cache[cache_key] = (response, datetime.utcnow())

    def search(
        self,
        query: str,
        search_depth: str = "advanced",
        include_answer: bool = True,
        use_cache: bool = True
    ) -> SearchResponse:
        """Execute web search with caching.

        Args:
            query: Search query
            search_depth: "basic" or "advanced" (Tavily parameter)
            include_answer: Include AI-generated answer summary
            use_cache: Use cached results if available

        Returns:
            SearchResponse with results and metadata

        Raises:
            RuntimeError: If Tavily client is not available
        """
        if not self.client:
            raise RuntimeError(
                "Tavily client not initialized. Install tavily-python and set TAVILY_API_KEY"
            )

        # Check cache first
        if use_cache:
            cached = self._get_cached(query)
            if cached:
                return cached

        # Execute search
        try:
            response = self.client.search(
                query=query,
                search_depth=search_depth,
                max_results=self.max_results,
                include_answer=include_answer
            )

            # Parse results
            results = [
                SearchResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    content=r.get("content", ""),
                    score=r.get("score", 0.0),
                    published_date=r.get("published_date")
                )
                for r in response.get("results", [])
            ]

            search_response = SearchResponse(
                query=query,
                results=results,
                answer=response.get("answer"),
                cached=False
            )

            # Cache results
            if use_cache:
                self._set_cache(query, search_response)

            return search_response

        except Exception as e:
            raise RuntimeError(f"Web search failed: {str(e)}")

    def search_salary_data(
        self,
        job_title: str,
        location: Optional[str] = None,
        experience_level: Optional[str] = None
    ) -> SearchResponse:
        """Search for salary data with context.

        Implements salary validation trigger from s1ngularity-web-search-integration.json
        """
        query_parts = [f"{job_title} salary"]
        if location:
            query_parts.append(f"in {location}")
        if experience_level:
            query_parts.append(f"{experience_level} level")
        query_parts.append("2024")

        query = " ".join(query_parts)
        return self.search(query, search_depth="advanced", include_answer=True)

    def search_technology_trends(self, technology: str) -> SearchResponse:
        """Search for technology adoption and market trends.

        Implements tech validation trigger from s1ngularity-web-search-integration.json
        """
        query = f"{technology} adoption trends market demand 2024"
        return self.search(query, search_depth="advanced", include_answer=True)

    def search_company_info(self, company_name: str) -> SearchResponse:
        """Search for company information and culture.

        Implements company research trigger from s1ngularity-web-search-integration.json
        """
        query = f"{company_name} company culture tech stack team size"
        return self.search(query, search_depth="advanced", include_answer=True)

    def validate_skill_demand(self, skill: str, industry: Optional[str] = None) -> SearchResponse:
        """Validate skill market demand.

        Implements skill validation from s1ngularity-web-search-integration.json
        """
        query_parts = [f"{skill} job market demand"]
        if industry:
            query_parts.append(f"in {industry}")
        query_parts.append("2024")

        query = " ".join(query_parts)
        return self.search(query, search_depth="basic", include_answer=True)


def get_web_search_tool() -> WebSearchTool:
    """Factory function to create WebSearchTool instance."""
    return WebSearchTool(
        api_key=os.getenv("TAVILY_API_KEY"),
        redis_url=os.getenv("REDIS_URL"),
        cache_ttl=int(os.getenv("WEB_SEARCH_CACHE_TTL", "3600")),
        max_results=int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
    )


__all__ = ["WebSearchTool", "SearchResult", "SearchResponse", "get_web_search_tool"]

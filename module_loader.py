"""Intelligent module loader for context-aware prompt injection.

Implements the "Intelligent Tool Selection" strategy from s1ngularity-reasoning-intelligence.json
Only loads relevant JSON modules based on task type to optimize context usage.
"""

from __future__ import annotations

import json
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TaskType(str, Enum):
    """Task types for intelligent module selection."""
    JD_ANALYSIS = "jd_analysis"
    RESUME_SCREENING = "resume_screening"
    BOOLEAN_SEARCH = "boolean_search"
    CANDIDATE_OUTREACH = "candidate_outreach"
    SALARY_RESEARCH = "salary_research"
    BIAS_CHECK = "bias_check"
    ANALYTICS = "analytics"
    GENERAL = "general"


class ModuleConfig(BaseModel):
    """Configuration for a system module."""
    name: str
    file_path: str
    task_types: List[TaskType]
    priority: int = 0  # Higher priority loaded first
    always_load: bool = False


class LoadedModule(BaseModel):
    """A loaded module with its content."""
    name: str
    content: Dict[str, Any]
    task_types: List[TaskType]


class ModuleLoader:
    """Intelligent module loader for S1NGULARITY system prompts.

    Implements context-aware loading:
    - ALWAYS loads: core-system (personality, guardrails)
    - CONDITIONALLY loads: task-specific modules
    - NEVER loads: irrelevant modules (saves tokens)
    """

    # Module configuration mapping
    MODULE_MAP: Dict[str, ModuleConfig] = {
        "core-system": ModuleConfig(
            name="core-system",
            file_path="s1ngularity-core-system.json",
            task_types=[],  # All tasks
            priority=100,
            always_load=True
        ),
        "jd-intelligence": ModuleConfig(
            name="jd-intelligence",
            file_path="s1ngularity-jd-intelligence.json",
            task_types=[TaskType.JD_ANALYSIS, TaskType.GENERAL],
            priority=90
        ),
        "resume-analysis": ModuleConfig(
            name="resume-analysis",
            file_path="s1ngularity-resume-analysis.json",
            task_types=[TaskType.RESUME_SCREENING, TaskType.GENERAL],
            priority=90
        ),
        "advanced-matching": ModuleConfig(
            name="advanced-matching",
            file_path="s1ngularity-advanced-matching.json",
            task_types=[TaskType.RESUME_SCREENING, TaskType.JD_ANALYSIS],
            priority=80
        ),
        "boolean-engine": ModuleConfig(
            name="boolean-engine",
            file_path="s1ngularity-boolean-engine-v1.json",
            task_types=[TaskType.BOOLEAN_SEARCH],
            priority=90
        ),
        "communications": ModuleConfig(
            name="communications",
            file_path="s1ngularity-communications.json",
            task_types=[TaskType.CANDIDATE_OUTREACH],
            priority=80
        ),
        "web-search": ModuleConfig(
            name="web-search",
            file_path="s1ngularity-web-search-integration.json",
            task_types=[TaskType.SALARY_RESEARCH, TaskType.GENERAL],
            priority=70
        ),
        "bias-detection": ModuleConfig(
            name="bias-detection",
            file_path="s1ngularity-bias-detection-compliance.json",
            task_types=[TaskType.BIAS_CHECK, TaskType.RESUME_SCREENING],
            priority=85
        ),
        "analytics": ModuleConfig(
            name="analytics",
            file_path="s1ngularity-analytics-insights.json",
            task_types=[TaskType.ANALYTICS],
            priority=70
        ),
        "reasoning": ModuleConfig(
            name="reasoning",
            file_path="s1ngularity-reasoning-intelligence.json",
            task_types=[TaskType.GENERAL],
            priority=95,
            always_load=True
        ),
        "context-awareness": ModuleConfig(
            name="context-awareness",
            file_path="s1ngularity-context-awareness.json",
            task_types=[TaskType.GENERAL],
            priority=90,
            always_load=True
        ),
        "output-templates": ModuleConfig(
            name="output-templates",
            file_path="s1ngularity-output-templates.json",
            task_types=[],  # All tasks
            priority=60,
            always_load=True
        ),
    }

    def __init__(self, modules_dir: Optional[Path] = None):
        """Initialize module loader.

        Args:
            modules_dir: Directory containing JSON module files (default: current dir)
        """
        self.modules_dir = modules_dir or Path.cwd()
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse JSON file."""
        full_path = self.modules_dir / file_path

        # Check cache first
        if file_path in self._cache:
            return self._cache[file_path]

        if not full_path.exists():
            raise FileNotFoundError(f"Module file not found: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        # Cache the content
        self._cache[file_path] = content
        return content

    def load_master_prompt(self) -> str:
        """Load the master TOON prompt file.

        Returns:
            Full content of s1ngularity-master-v3.toon
        """
        toon_path = self.modules_dir / "s1ngularity-master-v3.toon"
        if not toon_path.exists():
            raise FileNotFoundError(f"Master TOON file not found: {toon_path}")

        with open(toon_path, "r", encoding="utf-8") as f:
            return f.read()

    def load_modules_for_task(
        self,
        task_type: TaskType,
        include_general: bool = True
    ) -> List[LoadedModule]:
        """Load modules relevant to a specific task type.

        Args:
            task_type: Type of task being performed
            include_general: Include modules tagged for GENERAL tasks

        Returns:
            List of loaded modules, sorted by priority
        """
        loaded_modules = []

        for module_name, config in self.MODULE_MAP.items():
            # Load if: always_load OR task matches OR (include_general AND GENERAL in tasks)
            should_load = (
                config.always_load
                or task_type in config.task_types
                or (include_general and TaskType.GENERAL in config.task_types)
                or not config.task_types  # Empty task_types means "all tasks"
            )

            if should_load:
                try:
                    content = self._load_json_file(config.file_path)
                    loaded_modules.append(
                        LoadedModule(
                            name=config.name,
                            content=content,
                            task_types=config.task_types
                        )
                    )
                except FileNotFoundError:
                    print(f"Warning: Module file not found: {config.file_path}")
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON in {config.file_path}: {e}")

        # Sort by priority (higher first)
        module_priority = {name: cfg.priority for name, cfg in self.MODULE_MAP.items()}
        loaded_modules.sort(
            key=lambda m: module_priority.get(m.name, 0),
            reverse=True
        )

        return loaded_modules

    def build_system_prompt(
        self,
        task_type: TaskType,
        include_master: bool = True,
        include_modules: bool = True
    ) -> str:
        """Build complete system prompt for task type.

        Args:
            task_type: Type of task being performed
            include_master: Include master TOON prompt
            include_modules: Include task-specific JSON modules

        Returns:
            Formatted system prompt ready for LLM
        """
        prompt_parts = []

        # 1. Master TOON prompt (personality, core rules)
        if include_master:
            try:
                master_prompt = self.load_master_prompt()
                prompt_parts.append("# S1NGULARITY MASTER INSTRUCTIONS\n")
                prompt_parts.append(master_prompt)
                prompt_parts.append("\n\n")
            except FileNotFoundError:
                print("Warning: Master TOON file not found")

        # 2. Task-specific modules
        if include_modules:
            modules = self.load_modules_for_task(task_type)
            if modules:
                prompt_parts.append("# ACTIVE MODULES\n")
                for module in modules:
                    prompt_parts.append(f"\n## MODULE: {module.name.upper()}\n")
                    prompt_parts.append(json.dumps(module.content, indent=2))
                    prompt_parts.append("\n")

        return "".join(prompt_parts)

    def get_module_summary(self, task_type: TaskType) -> Dict[str, Any]:
        """Get summary of modules that would be loaded for a task.

        Useful for debugging and token estimation.
        """
        modules = self.load_modules_for_task(task_type)
        return {
            "task_type": task_type.value,
            "modules_loaded": [m.name for m in modules],
            "module_count": len(modules),
            "estimated_tokens": sum(
                len(json.dumps(m.content)) // 4  # Rough estimate: 4 chars = 1 token
                for m in modules
            )
        }


def get_module_loader() -> ModuleLoader:
    """Factory function to create ModuleLoader instance."""
    modules_dir = Path(os.getenv("MODULES_DIR", "."))
    return ModuleLoader(modules_dir=modules_dir)


# Example usage for testing
if __name__ == "__main__":
    loader = get_module_loader()

    # Test different task types
    for task_type in TaskType:
        print(f"\n{'='*60}")
        print(f"Task: {task_type.value}")
        print('='*60)
        summary = loader.get_module_summary(task_type)
        print(f"Modules: {', '.join(summary['modules_loaded'])}")
        print(f"Estimated tokens: {summary['estimated_tokens']:,}")


__all__ = ["ModuleLoader", "TaskType", "LoadedModule", "get_module_loader"]

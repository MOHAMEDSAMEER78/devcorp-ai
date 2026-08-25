"""System Prompt Loader for DSH Agent Profiles."""
from pathlib import Path
from typing import Optional


class PromptLoader:
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)

    def load_prompt(self, role_name: str) -> str:
        """Load markdown system prompt for a given agent role."""
        path = self.prompts_dir / f"{role_name}.md"
        if not path.exists():
            raise FileNotFoundError(f"System prompt for role '{role_name}' not found at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

"""A2A Agent Card Discovery and Skill Registry."""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentSkill(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    input_modes: List[str] = Field(default_factory=lambda: ["application/json"])
    output_modes: List[str] = Field(default_factory=lambda: ["application/json"])


class AgentCard(BaseModel):
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    skills: List[AgentSkill] = Field(default_factory=list)
    capabilities: Dict[str, Any] = Field(default_factory=dict)


class A2ARegistry:
    """Decentralized registry for discovering and routing across DSH A2A agent cards."""

    def __init__(self):
        self.cards: Dict[str, AgentCard] = {}

    def register_card(self, agent_name: str, card_data: Dict[str, Any]) -> AgentCard:
        card = AgentCard.model_validate(card_data)
        self.cards[agent_name] = card
        logger.info(f"Registered A2A Agent Card: {agent_name} ({len(card.skills)} skills)")
        return card

    def get_card(self, agent_name: str) -> Optional[AgentCard]:
        return self.cards.get(agent_name)

    def find_agents_by_skill(self, skill_id: str) -> List[AgentCard]:
        """Resolve all agents that expose a given functional skill."""
        matches = []
        for card in self.cards.values():
            if any(s.id == skill_id for s in card.skills):
                matches.append(card)
        return matches

    def list_all(self) -> List[AgentCard]:
        return list(self.cards.values())

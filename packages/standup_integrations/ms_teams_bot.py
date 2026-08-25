"""Microsoft Teams Bot Framework & Graph API Standup Integration."""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class MSTeamsStandupBot:
    """Automates sprint reviews and Adaptive Cards on Microsoft Teams."""

    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None):
        self.tenant_id = tenant_id
        self.client_id = client_id

    def create_adaptive_card_payload(self, sprint_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a rich Adaptive Card for MS Teams channel broadcast."""
        return {
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": f"DevCorp AI — Sprint {sprint_report.get('sprint_number', 1)} Review",
                    "weight": "Bolder",
                    "size": "Medium"
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {"title": "Stories Done", "value": str(len(sprint_report.get("completed_user_stories", [])))},
                        {"title": "Test Coverage", "value": f"{sprint_report.get('test_coverage_percent', 0.0)}%"},
                        {"title": "Total Cost", "value": f"${sprint_report.get('total_sprint_cost_usd', 0.0):.2f}"}
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.OpenUrl",
                    "title": "Open Standup Dashboard",
                    "url": "http://localhost:3000"
                }
            ]
        }

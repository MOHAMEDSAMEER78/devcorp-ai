"""Unit tests for Google Meet and Microsoft Teams Bots."""
from packages.standup_integrations import (
    GoogleMeetStandupBot,
    MSTeamsStandupBot,
)


def test_google_meet_bot():
    bot = GoogleMeetStandupBot()
    meeting = bot.schedule_standup_meeting(1, "Review Expense Tracker MVP")
    assert "meet.google.com" in meeting["join_url"]
    assert meeting["sprint"] == 1

    chat_msg = bot.format_chat_sprint_summary({
        "sprint_number": 1,
        "completed_user_stories": ["US-01"],
        "test_coverage_percent": 95.0,
        "total_tests_passed": 30,
        "total_sprint_cost_usd": 1.25
    })
    assert "DevCorp AI Sprint 1" in chat_msg


def test_ms_teams_bot():
    bot = MSTeamsStandupBot()
    card = bot.create_adaptive_card_payload({
        "sprint_number": 1,
        "completed_user_stories": ["US-01", "US-02"],
        "test_coverage_percent": 94.0,
        "total_sprint_cost_usd": 2.10
    })
    assert card["type"] == "AdaptiveCard"

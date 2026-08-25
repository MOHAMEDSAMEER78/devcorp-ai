"""Playwright Visual Journey Recorder with Interaction & Cursor Overlays."""
from pathlib import Path
from typing import Dict, Any

CURSOR_OVERLAY_SCRIPT = """
(() => {
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor-indicator';
    cursor.style.width = '20px';
    cursor.style.height = '20px';
    cursor.style.borderRadius = '50%';
    cursor.style.backgroundColor = 'rgba(255, 60, 60, 0.7)';
    cursor.style.border = '2px solid white';
    cursor.style.position = 'fixed';
    cursor.style.pointerEvents = 'none';
    cursor.style.zIndex = '999999';
    cursor.style.transition = 'transform 0.05s ease';
    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = `${e.clientX - 10}px`;
        cursor.style.top = `${e.clientY - 10}px`;
    });

    document.addEventListener('click', (e) => {
        const ripple = document.createElement('div');
        ripple.style.width = '40px';
        ripple.style.height = '40px';
        ripple.style.borderRadius = '50%';
        ripple.style.border = '2px solid rgba(255, 60, 60, 0.9)';
        ripple.style.position = 'fixed';
        ripple.style.left = `${e.clientX - 20}px`;
        ripple.style.top = `${e.clientY - 20}px`;
        ripple.style.pointerEvents = 'none';
        ripple.style.zIndex = '999998';
        ripple.style.animation = 'ripple-animation 0.4s ease-out forwards';
        document.body.appendChild(ripple);
        setTimeout(() => ripple.remove(), 400);
    });
})();
"""


class DemoRecorderConfig:
    """Configures recording parameters for high-definition demo synthesis."""

    def __init__(self, output_dir: str = "demo_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.viewport = {"width": 1280, "height": 720}
        self.slow_mo_ms = 500  # Pacing for human evaluation in standup


def get_cursor_script() -> str:
    return CURSOR_OVERLAY_SCRIPT

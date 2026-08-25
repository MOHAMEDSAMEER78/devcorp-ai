"""Packages recording outputs into a standardized ArtifactBundle."""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from packages.core.schemas.artifacts import ArtifactBundle, ArtifactItem


class DemoBundler:
    """Consolidates video replays, traces, and DOM snapshots into demo bundles."""

    def __init__(self, bundle_dir: str = "demo_output"):
        self.bundle_dir = Path(bundle_dir)

    def _compute_sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def package_bundle(self, sprint_id: str) -> ArtifactBundle:
        items: List[ArtifactItem] = []
        if self.bundle_dir.exists():
            for p in self.bundle_dir.rglob("*"):
                if p.is_file() and p.name != "manifest.json":
                    artifact_type = "mp4_video" if p.suffix == ".mp4" else "trace" if p.suffix == ".zip" else "screenshot"
                    items.append(ArtifactItem(
                        name=p.name,
                        artifact_type=artifact_type,
                        uri_or_path=str(p.resolve()),
                        sha256=self._compute_sha256(p)
                    ))

        bundle = ArtifactBundle(
            bundle_id=f"demo-{sprint_id}",
            sprint_id=sprint_id,
            items=items,
            manifest={"total_items": len(items), "sprint": sprint_id}
        )

        manifest_path = self.bundle_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(bundle.model_dump_json(indent=2))

        return bundle

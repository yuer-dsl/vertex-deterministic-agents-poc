"""
deterministic_agent_stub.py

A minimal, model-agnostic "agent" stub that demonstrates how a
constraint-driven, deterministic pipeline *could* be wired.

IMPORTANT:
- This file does NOT call Vertex AI, Gemini, or any external API.
- It simply shows how one might structure a deterministic execution path.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from constraint_loader import load_constraints
from multimodal_prompt_builder import build_prompts


@dataclass
class AgentConfig:
    """Configuration for the deterministic agent stub."""

    constraint_path: str
    reference_image: Optional[str] = None  # path or URL, left model-agnostic
    seed: Optional[int] = None


@dataclass
class AgentResult:
    """Result summary for the deterministic agent stub."""

    positive_prompt: str
    negative_prompt: str
    geometry_score: float
    semantic_drift_score: float
    aesthetic_score: float
    decision_log: Dict[str, Any]


class DeterministicAgent:
    """
    A stub showing how to structure a deterministic, constraint-driven agent.

    In a real system, `run()` would:
    - call a multi-modal model (e.g., Gemini / Vertex AI),
    - feed both reference image and structured prompts,
    - compute alignment scores,
    - enforce control thresholds.

    Here, we only:
    - load constraints,
    - build prompts deterministically,
    - return stub scores for demonstration.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self._constraints: Dict[str, Any] = {}

    def load(self) -> None:
        """Load and cache the constraint spec."""
        self._constraints = load_constraints(self.config.constraint_path)

    def run(self) -> AgentResult:
        """
        Run the deterministic agent stub.

        Returns
        -------
        AgentResult
            A summary including prompts and placeholder scores.
        """
        if not self._constraints:
            self.load()

        positive_prompt, negative_prompt = build_prompts(self._constraints)

        control = self._constraints.get("CONTROL", {})
        geometry_threshold = float(control.get("geometry_threshold", 0.8))
        semantic_drift_max = float(control.get("semantic_drift_max", 0.15))
        aesthetic_target = float(control.get("aesthetic_target", 0.87))

        # In a real system, the following scores would be computed against the
        # model's outputs. Here we simply echo the targets as "achieved" values
        # to show the intended structure.
        geometry_score = geometry_threshold
        semantic_drift_score = semantic_drift_max
        aesthetic_score = aesthetic_target

        decision_log: Dict[str, Any] = {
            "reference_image": self.config.reference_image,
            "seed": self.config.seed,
            "control": {
                "geometry_threshold": geometry_threshold,
                "semantic_drift_max": semantic_drift_max,
                "aesthetic_target": aesthetic_target,
            },
            "notes": [
                "This is a stub implementation.",
                "Integrate your own multimodal model in place of this.",
                "Scores are placeholders reflecting configured targets.",
            ],
        }

        return AgentResult(
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            geometry_score=geometry_score,
            semantic_drift_score=semantic_drift_score,
            aesthetic_score=aesthetic_score,
            decision_log=decision_log,
        )


def main() -> None:
    """
    Simple CLI entry point for manual testing.

    Example:
        python -m deterministic_agent_stub
    """
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Deterministic multimodal agent stub (no external API calls)."
    )
    parser.add_argument(
        "--constraints",
        type=str,
        default="examples/structured_multimodal_constraints.yaml",
        help="Path to constraint YAML file.",
    )
    parser.add_argument(
        "--ref-image",
        type=str,
        default=None,
        help="Optional reference image path or URL (not used in stub).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Optional seed for downstream deterministic components.",
    )

    args = parser.parse_args()

    agent = DeterministicAgent(
        AgentConfig(
            constraint_path=args.constraints,
            reference_image=args.ref_image,
            seed=args.seed,
        )
    )
    result = agent.run()

    print("=== POSITIVE PROMPT ===")
    print(result.positive_prompt)
    print("\n=== NEGATIVE PROMPT ===")
    print(result.negative_prompt)
    print("\n=== SCORES (STUB) ===")
    print(
        json.dumps(
            {
                "geometry_score": result.geometry_score,
                "semantic_drift_score": result.semantic_drift_score,
                "aesthetic_score": result.aesthetic_score,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    print("\n=== DECISION LOG (STUB) ===")
    print(json.dumps(result.decision_log, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

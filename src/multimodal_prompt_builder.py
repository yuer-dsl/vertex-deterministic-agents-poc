"""
multimodal_prompt_builder.py

Builds deterministic positive/negative prompts from a structured constraint spec.

The goal here is NOT to be clever or artistic, but:
- be config-driven,
- be deterministic,
- reflect the constraints in a human-readable way.

This module does not call any external APIs. It only returns prompt strings.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from utils.parse import get_nested


def build_positive_prompt(cfg: Dict[str, Any]) -> str:
    """
    Build a positive prompt string from the constraint dictionary.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Constraint specification.

    Returns
    -------
    str
        Deterministically constructed positive prompt.
    """
    parts: list[str] = []

    # --- INTENT ---
    intent_goal = get_nested(cfg, ["INTENT", "description"]) or get_nested(
        cfg, ["INTENT", "goal"]
    )
    if intent_goal:
        parts.append(str(intent_goal))

    # --- ANCHOR: body and pose ---
    body_ratio = get_nested(cfg, ["ANCHOR", "body_ratio", "target"])
    if body_ratio is not None:
        parts.append(
            f"subject has a solid, slightly above-average body proportion "
            f"(body ratio around {body_ratio})"
        )

    fat_dist = get_nested(cfg, ["ANCHOR", "fat_layer_distribution"])
    if isinstance(fat_dist, dict):
        abdomen_mode = fat_dist.get("abdomen")
        if abdomen_mode:
            parts.append(
                "abdomen shows natural, controlled volume with realistic compression"
            )

    pose_required = get_nested(cfg, ["ANCHOR", "pose_structure", "required"])
    if pose_required:
        parts.append("pose is consistent and stable, matching the reference posture")

    # --- FABRIC / CLOTHING ---
    fabric = get_nested(cfg, ["ANCHOR", "fabric_tension_model"]) or {}
    if isinstance(fabric, dict):
        folds = fabric.get("abdomen_cloth", {})
        folds_density = folds.get("folds_density")
        folds_direction = folds.get("folds_direction")
        if folds_density:
            parts.append(
                f"upper clothing has {folds_density.replace('_', ' ')} folds "
                "to reflect realistic fabric compression"
            )
        if folds_direction:
            parts.append(
                f"folds are primarily {folds_direction.replace('_', ' ')} "
                "for a natural drape"
            )

        thigh = fabric.get("thigh_cloth", {})
        thigh_tension = thigh.get("tension")
        if thigh_tension:
            parts.append(
                f"pants or lower clothing show {thigh_tension.replace('_', ' ')} "
                "fabric tension around the supporting legs"
            )

    # --- SCENE CONTEXT ---
    scene_env = get_nested(cfg, ["SCENE_CONTEXT", "environment"]) or "indoor setting"
    scene_elems = get_nested(cfg, ["SCENE_CONTEXT", "elements"]) or []
    parts.append(f"scene is a {scene_env}")
    if scene_elems:
        parts.append(
            "environment includes: " + ", ".join(str(e) for e in scene_elems)
        )

    # --- LIGHTING ---
    lighting_type = get_nested(cfg, ["SCENE_CONTEXT", "lighting", "type"])
    if lighting_type:
        parts.append(f"lighting is {lighting_type}, soft and coherent across the scene")

    # --- SEMANTIC_RULES / aesthetics ---
    must_optimize = get_nested(cfg, ["SEMANTIC_RULES", "must_optimize"]) or []
    if "texture_realism" in must_optimize:
        parts.append("textures are realistic and consistent, not over-smoothed")

    if "facial_symmetry" in must_optimize:
        parts.append("face is gently optimized for symmetry without changing identity")

    if "skin_tone_balance" in must_optimize:
        parts.append("skin tone is balanced and even, without heavy filters")

    # Final default: respect, realism, no caricature
    parts.append(
        "overall look is respectful, realistic and stable, with no cartoonish style"
    )

    # Join deterministically
    return ", ".join(parts)


def build_negative_prompt(cfg: Dict[str, Any]) -> str:
    """
    Build a negative prompt string from the constraint dictionary.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Constraint specification.

    Returns
    -------
    str
        Deterministically constructed negative prompt.
    """
    avoid = get_nested(cfg, ["SEMANTIC_RULES", "must_not"]) or []
    tokens: list[str] = []

    # Mapping from semantic flags → negative prompt phrases
    mapping = {
        "slim_body": "slim body, skinny body, unrealistic slimming, weight loss effect",
        "heavy_stylization": "cartoon, anime, 3d render, oil painting, cyberpunk style",
        "change_scene_to_outdoor": "outdoor scene, beach, forest, city street, sky view",
        "over_emphasize_belly_volume": (
            "exaggerated belly, fetishized belly, comically large abdomen"
        ),
    }

    for key in avoid:
        if key in mapping:
            tokens.append(mapping[key])

    # Always discourage generic artifacts if nothing is specified
    if not tokens:
        tokens.append(
            "distorted anatomy, extreme filters, low quality, artifacts, glitches"
        )

    return ", ".join(tokens)


def build_prompts(cfg: Dict[str, Any]) -> Tuple[str, str]:
    """
    Convenience wrapper to build both positive and negative prompts.

    Parameters
    ----------
    cfg : Dict[str, Any]
        Constraint specification.

    Returns
    -------
    Tuple[str, str]
        (positive_prompt, negative_prompt)
    """
    pos = build_positive_prompt(cfg)
    neg = build_negative_prompt(cfg)
    return pos, neg

# Deterministic Agents on Vertex AI — Minimal PoC

This repository explores whether **Vertex AI / Gemini agents**  
can operate under **deterministic, structure-driven execution constraints**,  
rather than relying solely on free-form LLM planning.

This is a **minimal, drop-in experimental PoC**.  
It is *not* a framework, *not* a replacement for any Google system.  
The goal is simply to test:

- Can multi-modal agents become more reproducible?
- Can config-driven constraints improve stability?
- Can we reduce identity drift and body-shape hallucination?
- Can agent execution paths be deterministic instead of emergent?

As multi-modal agents become more widely adopted, these questions  
become increasingly important for reliability, enterprise use cases,  
and predictable user experiences.

---

## 🔍 Background & Motivation

Current multi-modal LLM systems frequently exhibit:

- identity inconsistency  
- body-shape drift (especially for stocky/solid body types)  
- over-aggressive aesthetic optimization (unwanted “slimming”)  
- scene instability  
- non-reproducible execution paths  
- difficulty honoring structural constraints

This PoC tests whether a **structured YAML constraint layer**  
can improve stability for tasks such as:

- portrait generation  
- identity retention  
- pose preservation  
- fabric-tension consistency  
- scene continuity  
- lighting stability  

The same principles could apply to general-purpose multi-modal agents  
running on Gemini or Vertex AI.

---

## 📘 What This PoC Demonstrates

### ✔ Deterministic Behavior (Attempt)
A static execution plan derived from configuration instead of  
dynamic LLM improvisation.

### ✔ Constraint-Driven Prompt Construction
YAML → structured constraints → deterministic prompt builder.

### ✔ Multi-Modal Stability Testing
Focus on:

- body ratio  
- natural abdomen compression  
- fabric tension  
- folds direction  
- pose adherence  
- scene continuity  
- lighting coherence  

### ✔ Identity Preservation
Config-driven identity locking (high-level, model-agnostic).

---

## 📁 Repository Structure

vertex-deterministic-agents-poc/
│
├── README.md # You are here
├── LICENSE # MIT License
├── examples/
│ └── structured_multimodal_constraints.yaml
│
└── src/
├── constraint_loader.py
├── multimodal_prompt_builder.py
├── deterministic_agent_stub.py
└── utils/
└── parse.py

---

## 🧪 Example Constraint File

`examples/structured_multimodal_constraints.yaml`

```yaml
version: 0.1

profile:
  body_type: stocky
  goal: >
    Preserve identity, keep a solid/stocky body type,
    avoid slimming or over-beautification.

identity:
  lock_face: true
  lock_pose: true

geometry:
  body_ratio:
    target: 1.15
    tolerance: 0.05
  abdomen_behavior:
    allow_compression: true

fabric:
  top_cloth:
    folds_density: medium_high
    folds_direction: vertical_bias
  pants:
    tension: medium_high

scene:
  base: indoor_living_room
  required_elements:
    - sofa
    - window_blinds

lighting:
  type: soft_indoor_warm

rules:
  must_preserve:
    - identity
    - pose
    - body_ratio
  avoid:
    - slimming_body
    - heavy_stylization


This file acts as a high-level semantic constraint layer
for downstream prompt generation or agent behavior logic.

🛠 Minimal Prompt Builder

Pseudo-code for building deterministic prompts:

from constraint_loader import load_constraints
from multimodal_prompt_builder import build_prompts

cfg = load_constraints("examples/structured_multimodal_constraints.yaml")
positive, negative = build_prompts(cfg)

print("POSITIVE PROMPT:\n", positive)
print("NEGATIVE PROMPT:\n", negative)


The real implementations are intentionally minimal,
focusing on reproducibility over sophistication.

📌 Status

Early PoC.
More experiments coming soon, including:

deterministic plan stubs

multi-modal agent routing experiments

reproducibility benchmarking

Vertex AI / Gemini compatibility notes

constraint-layer evolution

📄 License

MIT License © 2025 Yuer

⭐ Final Notes

The purpose of this repository is to open a discussion around:

deterministic agent execution

constraint-driven multi-modal behavior

reproducibility in large-scale systems

As agent frameworks evolve (Gemini, Vertex AI, etc.),
deterministic and constraint-aware layers may become increasingly important
for stability and enterprise readiness.

More updates to follow.

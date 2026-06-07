"""Moderation classifier (stub) + the action mapping.

The real classifier (E7-1) is an LLM with a fast pre-filter, judging nuance and
(for audio) tone of voice. This stub encodes the *decision contract* and the
inviolable rule — pain and crisis are never blocked — so the safety invariant is
testable before the model lands.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Verdict(str, Enum):
    PAIN = "pain"
    HARM = "harm"
    CRISIS = "crisis"
    ALLOW = "allow"


class Action(str, Enum):
    ALLOW = "allow"          # content is published
    BLOCK = "block"          # other-directed harm; removed
    OFFER_HELP = "offer_help"  # crisis; gently surface the hotline, never punish


# The decision mapping is the safety-critical core. Note: PAIN and CRISIS are
# NEVER mapped to BLOCK. (FR-MOD-02, FR-HOT-07)
ACTION_FOR_VERDICT: dict[Verdict, Action] = {
    Verdict.PAIN: Action.ALLOW,
    Verdict.ALLOW: Action.ALLOW,
    Verdict.HARM: Action.BLOCK,
    Verdict.CRISIS: Action.OFFER_HELP,
}


def action_for(verdict: Verdict) -> Action:
    action = ACTION_FOR_VERDICT[verdict]
    # Defensive: assert the invariant even if the table is edited wrongly.
    if verdict in (Verdict.PAIN, Verdict.CRISIS) and action == Action.BLOCK:
        raise AssertionError("pain/crisis must never be blocked (FR-MOD-02)")
    return action


@dataclass
class Classification:
    verdict: Verdict
    action: Action
    confidence: float


def classify_text(text: str) -> Classification:
    """STUB heuristic — replace with the LLM classifier in E7-1.

    Deliberately conservative toward protecting pain. This is NOT production
    logic; it exists so the eval harness and the gateway can integrate now.
    """
    lowered = text.lower()

    crisis_markers = ("kill myself", "end it all", "suicide", "want to die", "can't go on")
    harm_markers = ("you're pathetic", "just give up", "you should die", "nobody likes you")

    if any(m in lowered for m in crisis_markers):
        verdict = Verdict.CRISIS
    elif any(m in lowered for m in harm_markers):
        verdict = Verdict.HARM
    elif any(m in lowered for m in ("worthless", "i can't do this", "hopeless", "i'm not okay")):
        verdict = Verdict.PAIN
    else:
        verdict = Verdict.ALLOW

    return Classification(verdict=verdict, action=action_for(verdict), confidence=0.5)

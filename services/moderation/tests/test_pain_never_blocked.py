"""E7-1 / E7-3 — pain is protected, crisis gets help, neither is ever blocked.

Requirements: FR-MOD-01, FR-MOD-02, FR-HOT-07. A failure here is CRITICAL.

This is a regression net for the single most dangerous failure mode: silencing
the exact person who most needs to be heard.
"""
import pytest

from moderation.classify import (
    ACTION_FOR_VERDICT,
    Action,
    Verdict,
    action_for,
    classify_text,
)

PAIN_EXAMPLES = [
    "I feel worthless and I can't do this anymore at work",
    "I'm not okay",
    "everything feels hopeless lately",
]

CRISIS_EXAMPLES = [
    "I want to die",
    "I keep thinking about suicide",
]

HARM_EXAMPLES = [
    "you're pathetic, just give up",
    "nobody likes you",
]


def test_action_table_never_blocks_pain_or_crisis():
    assert ACTION_FOR_VERDICT[Verdict.PAIN] != Action.BLOCK
    assert ACTION_FOR_VERDICT[Verdict.CRISIS] != Action.BLOCK


@pytest.mark.parametrize("text", PAIN_EXAMPLES)
def test_pain_is_allowed(text):
    c = classify_text(text)
    assert c.verdict == Verdict.PAIN
    assert c.action == Action.ALLOW


@pytest.mark.parametrize("text", CRISIS_EXAMPLES)
def test_crisis_offers_help_never_blocks(text):
    c = classify_text(text)
    assert c.verdict == Verdict.CRISIS
    assert c.action == Action.OFFER_HELP


@pytest.mark.parametrize("text", HARM_EXAMPLES)
def test_other_directed_harm_is_blocked(text):
    c = classify_text(text)
    assert c.verdict == Verdict.HARM
    assert c.action == Action.BLOCK


def test_action_for_rejects_a_mistaken_block_mapping():
    # If a future edit maps pain->block, action_for must refuse it.
    from moderation import classify

    original = classify.ACTION_FOR_VERDICT.copy()
    try:
        classify.ACTION_FOR_VERDICT[Verdict.PAIN] = Action.BLOCK
        with pytest.raises(AssertionError):
            action_for(Verdict.PAIN)
    finally:
        classify.ACTION_FOR_VERDICT.clear()
        classify.ACTION_FOR_VERDICT.update(original)

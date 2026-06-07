"""Unheard moderation service.

The three-way sort (FR-MOD-01):
  - PAIN   (self-directed distress) -> ALLOW & protect. NEVER blocked. (FR-MOD-02)
  - HARM   (cruelty aimed at someone else) -> BLOCK.
  - CRISIS (self-harm / suicide signals) -> OFFER HELP, never punish. (FR-HOT-07)

For audio comments, transcription is IN-MEMORY only and the transcript is
destroyed after the classifier reads it. (FR-MOD-04, NFR-PRIV-01)

The #1 job is distinguishing self-directed pain (protect) from other-directed
harm (remove). A defect that blocks pain is CRITICAL. (E7, RISK-MOD)
"""

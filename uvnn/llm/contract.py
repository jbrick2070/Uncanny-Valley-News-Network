from __future__ import annotations
from typing import TypedDict, List

class ShotLedger(TypedDict):
    shot_id: int
    visual_action: str
    audio_cues: str

class SegmentLedger(TypedDict):
    segment_title: str
    segment_type: str
    shots: List[ShotLedger]

# This is the exact JSON structure we instruct the LLM to provide.
LEDGER_SCHEMA_PROMPT = """
You MUST respond ONLY with a valid JSON object matching this schema:
{
  "segment_title": "A short, uncanny title for the segment",
  "segment_type": "breaking_news | commercial | public_access | weather",
  "shots": [
    {
      "shot_id": 1,
      "visual_action": "Description of the visual action for the video generator (e.g. 'Furious anchor slamming desk...')",
      "audio_cues": "Description of the native audio to generate (e.g. 'Loud yelling, paper rustling, synth drone...')"
    }
  ]
}
"""

from __future__ import annotations
import json
import re
from typing import Any

from .provider_base import LLMProvider
from .contract import SegmentLedger, LEDGER_SCHEMA_PROMPT

_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)

def extract_json_object(text: str) -> dict[str, Any]:
    """Recover the JSON object a model meant to send. (Stolen from OTR local_model_provider)"""
    match = _FENCE_RE.search(text)
    if match:
        text = match.group(1)
        
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise ValueError("No JSON object found in text")
        
    clean_text = text[start_idx:end_idx+1]
    return json.loads(clean_text)


class PromptSynthesizer:
    """
    Transforms raw text into an OTR-style Segment Ledger for the 80s UHF broadcast.
    """
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
        self.system_prompt = (
            "You are a 'Ledger Script Writer' for an uncanny 1980s UHF public access channel called 'UVNN'.\n"
            "Rules:\n"
            "1. De-identify content: Replace real-world brand names, real politicians, real celebrities, or exact locations "
            "with bizarre, satirical, uncanny 80s alternatives (e.g. 'Apple' -> 'Orchard Micro-Logics').\n"
            "2. Break the concept down into 2 to 3 distinct 'shots' that tell a multi-modal story.\n"
            "3. For each shot, provide highly dynamic 'visual_action' (including 'VHS tracking distortion', 'grainy 80s broadcast footage') "
            "and highly specific 'audio_cues' (e.g., 'talking loudly', 'microphone feedback', 'frantic synth').\n"
            + LEDGER_SCHEMA_PROMPT
        )

    def synthesize_ledger(self, raw_concept: str) -> SegmentLedger:
        prompt = f"Convert this idea into a UVNN structured broadcast segment ledger:\n\n{raw_concept}"
        
        # We might need a small retry loop, but for now we try once
        raw_output = self.provider.generate(self.system_prompt, prompt)
        
        try:
            parsed = extract_json_object(raw_output)
            # Basic validation
            if "shots" not in parsed:
                raise ValueError("Missing 'shots' array in output")
            return parsed
        except Exception as e:
            print(f"[PromptSynthesizer] Failed to extract ledger: {e}")
            print(f"[PromptSynthesizer] Raw Output was:\n{raw_output}")
            
            # Fallback ledger so the engine never halts
            return {
                "segment_title": "Emergency Broadcast",
                "segment_type": "breaking_news",
                "shots": [
                    {
                        "shot_id": 1,
                        "visual_action": "Emergency technical difficulties card, strange geometric shapes, heavy VHS distortion.",
                        "audio_cues": "Loud unbroken sine wave tone, faint whispering, static."
                    }
                ]
            }

from __future__ import annotations
import time
import sys

from uvnn.llm.local_openai import LocalOpenAIProvider
from uvnn.llm.prompt_synthesizer import PromptSynthesizer
from uvnn.visual.backend_ltx25 import LTX25Backend
from uvnn.sources.commercial_bank import get_random_commercial
from uvnn.sources.rss_feeder import RSSFeeder

def main():
    print("Initializing Uncanny Valley News Network (UVNN) Engine...")
    
    # 1. Setup Upstream Prompting
    provider = LocalOpenAIProvider(base_url="http://127.0.0.1:1234/v1")
    synthesizer = PromptSynthesizer(provider)
    
    # 2. Setup Video Backend
    backend = LTX25Backend()
    
    # 3. Setup Sources
    rss_feeder = RSSFeeder()
    
    print("UVNN Broadcast Director Online. Commencing 24/7 stream...")
    
    segment_count = 0
    while True:
        # Simple broadcast wheel: News -> Commercial -> News -> Promo -> repeat
        if segment_count % 2 == 0:
            print(f"\n=== [Director] Segment {segment_count}: Fetching News ===")
            raw_concept = rss_feeder.get_random_headline()
        else:
            print(f"\n=== [Director] Segment {segment_count}: Fetching Commercial/Promo ===")
            raw_concept = get_random_commercial()
            
        print(f"[Director] Raw Concept: {raw_concept}")
        
        # De-identify and synthesize into an OTR-style structured Ledger
        print("[Director] Synthesizing multi-modal ledger via LLM...")
        ledger = synthesizer.synthesize_ledger(raw_concept)
        
        print(f"[Director] Successfully authored '{ledger.get('segment_title', 'Unknown')}' ({len(ledger.get('shots', []))} shots)")
        
        # Process Shots Sequentially
        for shot in ledger.get("shots", []):
            shot_id = shot.get("shot_id", 0)
            print(f"\n  -> [Director] Dispatching Shot {shot_id} to Video Engine...")
            
            # Combine the visual action and audio cues into the final engine prompt
            # LTX-2.5 generates audio natively based on the prompt description.
            combined_prompt = f"{shot.get('visual_action', '')}, {shot.get('audio_cues', '')}, highly detailed, 4k"
            print(f"     Prompt: {combined_prompt}")
            
            # Dispatch to Video Backend
            output_path = backend.generate_segment(combined_prompt)
            
            if output_path:
                print(f"     [+] Successfully broadcasted shot {shot_id}: {output_path}")
            else:
                print(f"     [-] Shot {shot_id} generation failed or skipped.")
                
            # Brief pause between shots in the same segment
            time.sleep(1)
            
        segment_count += 1
        
        # Delay between segments
        print("\n[Director] Segment complete. Moving to next in broadcast wheel...")
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUVNN Broadcast Engine shutting down. Off-air.")
        sys.exit(0)

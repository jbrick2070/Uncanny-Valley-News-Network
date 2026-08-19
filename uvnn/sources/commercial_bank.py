from __future__ import annotations
import random

COMMERCIAL_CONCEPTS = [
    "A chaotic infomercial for a kitchen blender that claims to also fold your laundry. The host is sweating profusely and shouting.",
    "A bizarre local ad for a personal injury attorney who is standing in a swamp, promising to sue the swamp monsters.",
    "A late-night car dealership commercial where the owner is fighting a giant inflatable gorilla while listing low prices.",
    "A cheesy promo for an upcoming B-movie creature feature about a giant mutated lobster attacking a suburban mall.",
    "An urgent, poorly-lit public access broadcast of a man wearing tinfoil explaining how the neighborhood birds are recording everything.",
    "A local bowling alley advertisement featuring terrible green screen effects of a man bowling strikes in outer space.",
    "A frantic infomercial selling a hair growth tonic that clearly just glues carpet to your head. The demonstration goes horribly wrong.",
    "A mattress liquidation sale commercial where the announcer sounds like he is holding back tears, begging people to take the mattresses.",
    "A 1-900 psychic hotline promo featuring a mysterious woman floating in a void of 80s computer graphics.",
    "A technical difficulties screen with a very unhelpful, vaguely threatening voiceover apologizing for the 'temporal anomaly'."
]

def get_random_commercial() -> str:
    return random.choice(COMMERCIAL_CONCEPTS)

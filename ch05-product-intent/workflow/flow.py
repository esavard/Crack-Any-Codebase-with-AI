"""Ch5 flow: fetch the repo, then run all four product story extractions plus
an optional illustration.

The four LLM extractions are independent of each other (each just needs the
codebase dump). Keep them sequential because cache hits make second runs
instant anyway, and sequential console output is easier to debug.

IllustratePain runs after VariantSentence because it needs both the pain and
the variant. It's the only node that may be skipped (no GEMINI_API_KEY) or
fail silently; the rest of the story still renders without an image.
"""
from pocketflow import Flow
from nodes import (FetchRepo, PainScene, VariantSentence,
                   CompetitivePositioning, SurprisesAndAbsences,
                   IllustratePain)


def create_product_story_flow() -> Flow:
    fetch = FetchRepo()
    pain = PainScene()
    variant = VariantSentence()
    illustrate = IllustratePain()
    positioning = CompetitivePositioning()
    surprises = SurprisesAndAbsences()

    fetch >> pain >> variant >> illustrate >> positioning >> surprises
    return Flow(start=fetch)

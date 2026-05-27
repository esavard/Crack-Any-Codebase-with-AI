"""Ch5 flow: fetch the repo, then run all four product story extractions sequentially.

The four extractions are independent of each other (each just needs the codebase),
so we could in principle parallelize. We keep them sequential because:
  1. Cache hits make the second run instant anyway.
  2. Sequential output is easier to follow when debugging.
  3. PocketFlow's parallel BatchNode is built for many items of the same shape,
     not four distinct nodes.
"""
from pocketflow import Flow
from nodes import (FetchRepo, PainScene, VariantSentence,
                   CompetitivePositioning, SurprisesAndAbsences)


def create_product_story_flow() -> Flow:
    fetch = FetchRepo()
    pain = PainScene()
    variant = VariantSentence()
    positioning = CompetitivePositioning()
    surprises = SurprisesAndAbsences()

    fetch >> pain >> variant >> positioning >> surprises
    return Flow(start=fetch)

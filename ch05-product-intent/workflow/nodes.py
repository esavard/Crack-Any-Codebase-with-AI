"""Ch5 nodes: extract a product story from a codebase.

Four independent extractions (§5.1 to §5.4 of the chapter):
  - Pain scene (Curse of Knowledge)
  - Variant sentence (reproduce-it test)
  - Competitive positioning (counter-positioning)
  - Surprises and absences (Slack-and-Flickr signals)

Each is its own node with max_retries so bad LLM output retries cleanly.
"""
import os, re, sys, yaml
from pocketflow import Node

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from utils import call_llm, crawl  # noqa: E402

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts')


def load_prompt(name):
    return open(os.path.join(PROMPTS_DIR, name)).read()


def parse_yaml(text):
    m = re.search(r"```yaml\s*\n(.*?)```", text, re.DOTALL)
    assert m, f"LLM response missing ```yaml fence. Got:\n{text[:500]}"
    return yaml.safe_load(m.group(1))


class FetchRepo(Node):
    def prep(self, shared):
        return shared["repo_path"]

    def exec(self, repo_path):
        return crawl(repo_path)

    def post(self, shared, prep_res, exec_res):
        shared["codebase"] = exec_res
        print(f"  Crawled {len(exec_res):,} chars from {prep_res}")


class PainScene(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("pain-scene.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        return call_llm(prompt).strip()

    def post(self, shared, prep_res, exec_res):
        shared["pain"] = exec_res
        print(f"  Pain scene ({len(exec_res)} chars)")


class VariantSentence(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("variant-sentence.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        return call_llm(prompt).strip()

    def post(self, shared, prep_res, exec_res):
        shared["variant"] = exec_res
        print(f"  Variant sentence: {exec_res[:80]}...")


class CompetitivePositioning(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("competitive-positioning.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        result = parse_yaml(call_llm(prompt))
        assert "competitors" in result and len(result["competitors"]) >= 2
        assert "dimensions" in result and len(result["dimensions"]) >= 3
        for k in ("sacrifices", "gains", "why_incumbents_cannot_copy"):
            assert k in result, f"missing {k} in positioning"
        # Each cell must be {verdict, detail}. Reject the old flat-string shape so a retry kicks in.
        for c in result["competitors"]:
            for cell in c.get("cells", []):
                assert isinstance(cell, dict) and "verdict" in cell and "detail" in cell, \
                    f"cell missing verdict/detail in {c['name']}: {cell!r}"
        return result

    def post(self, shared, prep_res, exec_res):
        shared["positioning"] = exec_res
        print(f"  Positioning: {len(exec_res['competitors'])} competitors, "
              f"{len(exec_res['dimensions'])} dimensions")


class SurprisesAndAbsences(Node):
    def __init__(self):
        super().__init__(max_retries=3, wait=2)

    def prep(self, shared):
        return load_prompt("surprises-and-absences.md").format(codebase=shared["codebase"])

    def exec(self, prompt):
        result = parse_yaml(call_llm(prompt))
        assert "present" in result and "absent" in result
        for p in result["present"]:
            for k in ("headline", "where", "bet"):
                assert k in p, f"present item missing {k}: {p!r}"
        for a in result["absent"]:
            for k in ("headline", "evidence", "tradeoff"):
                assert k in a, f"absent item missing {k}: {a!r}"
        return result

    def post(self, shared, prep_res, exec_res):
        shared["surprises"] = exec_res
        print(f"  Surprises: {len(exec_res['present'])} present, "
              f"{len(exec_res['absent'])} absent")

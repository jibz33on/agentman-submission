import json
import sys
import os
from statistics import mean

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from helpers import add_user_message, chat

SKILL_PROMPT = open(os.path.join(os.path.dirname(__file__), "..", "skill.md")).read()

REQUIRED_SECTIONS = [
    "SUSPICIOUS_ACTIVITY_DESCRIPTION:",
    "INDICATORS_OF_SUSPICION:",
    "PRIOR_RELATIONSHIP:",
    "RECOMMENDED_ACTION:",
    "THRESHOLD CHECK",
    "ANALYST REMINDER",
]

CRIME_CONCLUSIONS = [
    "committed fraud",
    "is guilty",
    "is a criminal",
    "is a fraudster",
    "committed a crime",
    "is laundering",
]


def run_skill(case_input: str) -> str:
    messages = []
    add_user_message(messages, f"{SKILL_PROMPT}\n\nTransaction input:\n\n{case_input}")
    return chat(messages, max_tokens=2000)


def grade_rule_based(output: str, case: dict) -> dict:
    output_lower = output.lower()
    scores = {}

    sections_present = all(s in output for s in REQUIRED_SECTIONS)
    scores["sections_present"] = 10 if sections_present else 1

    no_crime_conclusions = not any(c in output_lower for c in CRIME_CONCLUSIONS)
    scores["no_crime_conclusions"] = 10 if no_crime_conclusions else 1

    no_first_person = not any(w in output_lower for w in [" i ", " we ", "our analysts"])
    scores["no_first_person"] = 10 if no_first_person else 1

    expected = case["expected_action"]
    rec = output_lower
    if expected == "freeze":
        correct_action = "freeze" in rec or "immediately" in rec
    else:
        correct_action = "monitor" in rec and "freeze" not in rec
    scores["correct_action"] = 10 if correct_action else 1

    rule_score = mean(scores.values())
    return {"scores": scores, "rule_score": rule_score}


def grade_by_model(case: dict, output: str) -> dict:
    prompt = f"""You are an expert AML compliance reviewer. Grade this SAR narrative draft.

Case description: {case["description"]}

SAR Output:
{output}

Score on these criteria (1-10 each):
1. regulatory_language: Correct use of regulatory terminology and typology codes
2. flag_mapping: FraudSentinel flags correctly translated to regulatory language
3. insight_quality: Reasoning explains WHY indicators are suspicious, not just lists them
4. analyst_notes_used: Analyst notes (if any) incorporated appropriately

Return only a JSON object:
{{
  "regulatory_language": <score>,
  "flag_mapping": <score>,
  "insight_quality": <score>,
  "analyst_notes_used": <score>,
  "model_score": <average of above>,
  "reasoning": "<one sentence on biggest strength and weakness>"
}}"""

    messages = []
    add_user_message(messages, prompt)
    result = chat(messages)
    result = result.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(result)


def run_case(case: dict) -> dict:
    print(f"\n--- {case['id']} ---")
    print(f"    {case['description']}")

    output = run_skill(case["input"])
    rule_result = grade_rule_based(output, case)
    model_result = grade_by_model(case, output)

    combined = (rule_result["rule_score"] + model_result["model_score"]) / 2

    print(f"    Rule score:  {rule_result['rule_score']:.1f}")
    print(f"    Model score: {model_result['model_score']:.1f}")
    print(f"    Combined:    {combined:.1f}")
    print(f"    Reasoning:   {model_result['reasoning']}")

    return {
        "id": case["id"],
        "output": output,
        "rule_scores": rule_result["scores"],
        "rule_score": rule_result["rule_score"],
        "model_scores": model_result,
        "model_score": model_result["model_score"],
        "combined_score": combined,
    }


def run_eval(dataset: list) -> list:
    results = [run_case(case) for case in dataset]
    avg = mean(r["combined_score"] for r in results)
    print(f"\n{'='*40}")
    print(f"AVERAGE SCORE: {avg:.2f} / 10")
    print(f"{'='*40}\n")
    return results


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "dataset.json")) as f:
        dataset = json.load(f)

    results = run_eval(dataset)

    output_path = os.path.join(os.path.dirname(__file__), "last_run.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full results saved to eval/last_run.json")

import ast
import json
import re
from statistics import mean
from helpers import add_user_message, chat


def validate_python(output: str) -> bool:
    try:
        ast.parse(output)
        return True
    except SyntaxError:
        return False


def validate_json(output: str) -> bool:
    try:
        json.loads(output)
        return True
    except json.JSONDecodeError:
        return False


def validate_regex(output: str) -> bool:
    try:
        re.compile(output)
        return True
    except re.error:
        return False


def grade_syntax(output: str, test_case: dict) -> int:
    fmt = test_case.get("format", "")
    if fmt == "python":
        return 10 if validate_python(output) else 1
    if fmt == "json":
        return 10 if validate_json(output) else 1
    if fmt == "regex":
        return 10 if validate_regex(output) else 1
    return 5


def run_prompt(test_case):
    prompt = f"""
Write a solution for the following task:

Here are examples of tasks with ideal responses:

<sample_input>
Write a Python function that extracts the region from an AWS ARN string.
</sample_input>

<ideal_output>
def extract_region(arn: str) -> str:
    return arn.split(":")[3]
</ideal_output>

<sample_input>
Create a JSON object representing an AWS S3 bucket policy that allows public read access.
</sample_input>

<ideal_output>
{{
  "Version": "2012-10-17",
  "Statement": [{{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }}]
}}
</ideal_output>

<sample_input>
Write a regex pattern that matches an AWS Lambda function name (1-64 characters, letters, numbers, hyphens, underscores).
</sample_input>

<ideal_output>
^[a-zA-Z0-9_-]{{1,64}}$
</ideal_output>

Each example is ideal because it returns the raw solution only — no markdown fences, no explanation, just the working code, JSON, or regex.

Now solve this task:

<task>
{test_case["task"]}
</task>

Guidelines:
- Return raw code only, no markdown fences or backticks
- Write a complete, working solution
- Use only standard library imports where possible
"""
    messages = []
    add_user_message(messages, prompt)
    return chat(messages)


def grade_by_model(test_case, output):
    eval_prompt = f"""
You are an expert code reviewer. Evaluate this AI-generated solution.

Task: {test_case["task"]}
Solution: {output}

Return only a JSON object with these fields:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your assessment
- "score": A number between 1-10
"""
    messages = []
    add_user_message(messages, eval_prompt)

    eval_text = chat(messages)
    eval_text = eval_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(eval_text)


def run_test_case(test_case):
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case, output)
    syntax_score = grade_syntax(output, test_case)
    score = (model_grade["score"] + syntax_score) / 2

    print(f"✓ {test_case['task'][:50]}... model: {model_grade['score']} syntax: {syntax_score} combined: {score}")

    return {
        "output": output,
        "test_case": test_case,
        "model_score": model_grade["score"],
        "syntax_score": syntax_score,
        "score": score,
        "reasoning": model_grade["reasoning"],
        "strengths": model_grade["strengths"],
        "weaknesses": model_grade["weaknesses"],
    }


def run_eval(dataset):
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"\nAverage score: {average_score}")

    return results


if __name__ == "__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    results = run_eval(dataset)
    print(json.dumps(results, indent=2))

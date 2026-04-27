"""
Generate evaluation dataset using Claude Haiku
Implements the prefilling + stop sequences technique
"""

import json
from helpers import add_user_message, add_assistant_message, chat

def generate_dataset(num_tasks=3):
    """
    Generate test dataset for AWS code generation tasks
    
    Returns:
        List of task dictionaries
    """
    prompt = f"""
Generate an evaluation dataset for prompt evaluation. The dataset will be used 
to evaluate prompts that generate Python, JSON, or Regex specifically for 
AWS-related tasks.

Generate an array of JSON objects, each representing a task that requires 
Python, JSON, or a Regex to complete.

Example output:
```json
[
  {{
    "task": "Description of task",
    "format": "python"
  }},
  ...additional
]
```

The "format" field must be one of: "python", "json", or "regex".

Guidelines:
* Focus on tasks that can be solved by writing a single Python function, 
  a single JSON object, or a single regex
* Focus on tasks that do not require writing much code
* Make tasks realistic and varied

Please generate {num_tasks} objects.
"""
    
    # Build the conversation
    messages = []
    add_user_message(messages, prompt)
    
    # PREFILLING: Start Claude's response with the opening of JSON
    add_assistant_message(messages, "```json")
    
    # Use Haiku for dataset generation (faster and cheaper)
    # Stop at closing backticks to get clean JSON
    response_text = chat(
        messages, 
        model="claude-haiku-4-5-20251001",
        stop_sequences=["```"]
    )
    
    # Parse the JSON
    dataset = json.loads(response_text)
    
    return dataset

def save_dataset(dataset, filename="dataset.json"):
    """Save dataset to JSON file"""
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)
    print(f"✓ Saved {len(dataset)} tasks to {filename}")

if __name__ == "__main__":
    print("Generating evaluation dataset...")
    
    # Generate 5 test tasks
    dataset = generate_dataset(num_tasks=5)
    
    # Show what we generated
    print("\nGenerated tasks:")
    for i, task in enumerate(dataset, 1):
        print(f"{i}. {task['task']}")
    
    # Save to file
    save_dataset(dataset)
    
    print("\n✓ Dataset generation complete!")
def generate(data):
    topic=data.get("topic","Topic")
    return f'''# Assignment: {topic}

## Instructions
- Submit original work.
- Use examples and references where appropriate.

## Tasks
1. Explain the fundamental concepts.
2. Analyze a practical application.
3. Compare advantages and limitations.
4. Present your conclusion.

## Evaluation Rubric
| Criteria | Marks |
|---|---:|
| Understanding | 25 |
| Analysis | 25 |
| Examples | 25 |
| Presentation | 25 |'''

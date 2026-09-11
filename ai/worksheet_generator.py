def generate(data):
    topic=data.get("topic","Topic")
    return f'''# Worksheet: {topic}

Name: ____________   Date: ____________

## Part A — Fill in the blanks
1. The main concept of {topic} is ____________.

## Part B — Short Answer
2. Explain {topic} in your own words.
3. Give two examples.

## Part C — Application
4. Solve a real-world problem related to {topic}.'''

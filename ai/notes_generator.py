def generate(data):
    topic=data.get("topic","Topic")
    return f'''# Study Notes: {topic}

## Definition
A concise explanation of the topic.

## Key Points
- Important concept one
- Important concept two
- Practical application

## Quick Revision
Remember the definition, process, applications and limitations.

## Practice
Write three examples and explain one real-world use case.'''

def generate(data):
    topic=data.get("topic","Topic"); marks=data.get("marks","50"); difficulty=data.get("difficulty","Mixed")
    return f'''# Question Paper: {topic}
**Total Marks: {marks} | Difficulty: {difficulty}**

## Section A — Short Questions
1. Define the key concept of {topic}. (2)
2. List two important features. (2)
3. Give one real-world application. (2)

## Section B — Medium Questions
4. Explain the working process with an example. (5)
5. Compare two important concepts. (5)

## Section C — Long Questions
6. Analyze the importance and limitations of {topic}. (10)

# Answer Key
Provide conceptually correct definitions, explanations, examples and analysis aligned to the syllabus.'''

def generate(data):
    topic=data.get("topic","Topic"); subject=data.get("subject","General"); grade=data.get("grade","All")
    return f'''# Lesson Plan: {topic}

## Subject
{subject} | Grade: {grade}

## Learning Objectives
- Explain the core concepts of {topic}.
- Apply knowledge through guided activities.
- Evaluate understanding through assessment.

## Introduction (10 minutes)
Activate prior knowledge with a discussion and real-world example.

## Main Teaching Activities
1. Explain key concepts.
2. Demonstrate with examples.
3. Collaborative student activity.
4. Guided practice.

## Assessment
Exit ticket, short quiz, and teacher observation.

## Homework
Create a concise summary and solve practice questions.'''

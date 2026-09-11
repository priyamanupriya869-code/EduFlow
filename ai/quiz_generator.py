def generate(data):
    topic=data.get("topic","Topic"); count=int(data.get("count",5))
    lines=[f"# Quiz: {topic}", ""]
    for i in range(1,count+1):
        lines += [f"## Question {i}", f"What is an important concept related to {topic}?", "A. Option One", "B. Option Two", "C. Option Three", "D. Option Four", "**Answer:** B", ""]
    return "\n".join(lines)

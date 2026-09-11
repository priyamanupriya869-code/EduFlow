def generate(data):
    topic=data.get("topic","Topic"); slides=int(data.get("slides",8))
    sections=["Title","Introduction","Core Concepts","How It Works","Applications","Advantages","Challenges","Future Scope","Conclusion"]
    out=[f"# Presentation: {topic}"]
    for i in range(slides):
        title=sections[i] if i<len(sections) else f"Key Insight {i+1}"
        out += [f"## Slide {i+1}: {title}", f"- Key point about {topic}", "- Supporting explanation", "- Example or visual suggestion", ""]
    return "\n".join(out)

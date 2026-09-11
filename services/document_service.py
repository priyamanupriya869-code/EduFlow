import json
from database import db
from database.models import Document, Activity

def save_document(user_id,title,tool,content,metadata=None):
    doc=Document(user_id=user_id,title=title,tool=tool,content=content,metadata_json=json.dumps(metadata or {}))
    db.session.add(doc)
    db.session.add(Activity(user_id=user_id, action=f"Created {tool}: {title}"))
    db.session.commit()
    return doc

def update_document(doc,title,content):
    doc.title=title; doc.content=content
    db.session.commit()
    return doc

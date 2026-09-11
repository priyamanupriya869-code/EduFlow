from sqlalchemy import func
from database import db
from database.models import Document

def user_analytics(user_id):
    total=Document.query.filter_by(user_id=user_id).count()
    rows=db.session.query(Document.tool, func.count(Document.id)).filter_by(user_id=user_id).group_by(Document.tool).all()
    return {"total":total,"tools":dict(rows)}

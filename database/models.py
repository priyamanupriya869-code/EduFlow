from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(180), unique=True, nullable=False)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(30), default="Teacher")
    institution=db.Column(db.String(150))
    bio=db.Column(db.Text)
    onboarded=db.Column(db.Boolean, default=False)
    is_admin=db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    documents=db.relationship("Document", backref="owner", lazy=True, cascade="all, delete-orphan")
    def set_password(self,password): self.password_hash=generate_password_hash(password)
    def check_password(self,password): return check_password_hash(self.password_hash,password)

class Document(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title=db.Column(db.String(250), nullable=False)
    tool=db.Column(db.String(60), nullable=False)
    content=db.Column(db.Text, nullable=False, default="")
    metadata_json=db.Column(db.Text, default="{}")
    favorite=db.Column(db.Boolean, default=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Activity(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action=db.Column(db.String(250), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

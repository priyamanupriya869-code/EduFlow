import os, importlib
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from database import db
from database.models import User, Document, Activity
from services.document_service import save_document, update_document
from services.analytics_service import user_analytics
from services import export_service

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager=LoginManager(app)
login_manager.login_view="login"

os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
os.makedirs(app.config["EXPORT_FOLDER"],exist_ok=True)

@login_manager.user_loader
def load_user(uid): return db.session.get(User,int(uid))

@app.context_processor
def inject_tools():
    return {"tools":[("lesson_planner","Lesson Planner","📚"),("question_paper","Question Paper","📝"),("quiz","Quiz Generator","❓"),("assignment","Assignment","📋"),("ppt_generator","PPT Generator","🎞️"),("notes_generator","Notes Generator","📖"),("worksheet_generator","Worksheet Generator","📄")]}

@app.route("/")
def index(): return render_template("index.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); email=request.form.get("email","").lower().strip(); password=request.form.get("password","")
        if not name or not email or len(password)<6: flash("Enter valid details. Password must be at least 6 characters.","error")
        elif User.query.filter_by(email=email).first(): flash("Email already registered.","error")
        else:
            u=User(name=name,email=email); u.set_password(password); db.session.add(u); db.session.commit()
            login_user(u); return redirect(url_for("onboarding"))
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=User.query.filter_by(email=request.form.get("email","").lower()).first()
        if u and u.check_password(request.form.get("password","")):
            login_user(u); return redirect(url_for("dashboard"))
        flash("Invalid email or password.","error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout(): logout_user(); return redirect(url_for("index"))

@app.route("/onboarding",methods=["GET","POST"])
@login_required
def onboarding():
    if request.method=="POST":
        current_user.role=request.form.get("role","Teacher")
        current_user.institution=request.form.get("institution","")
        current_user.bio=request.form.get("bio","")
        current_user.onboarded=True; db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("onboarding.html")

@app.route("/dashboard")
@login_required
def dashboard():
    recent=Document.query.filter_by(user_id=current_user.id).order_by(Document.updated_at.desc()).limit(6).all()
    stats=user_analytics(current_user.id)
    return render_template("dashboard.html",recent=recent,stats=stats)

@app.route("/tool/<tool>",methods=["GET","POST"])
@login_required
def tool(tool):
    allowed={"lesson_planner":"lesson_planner","question_paper":"question_generator","quiz":"quiz_generator","assignment":"assignment_generator","ppt_generator":"ppt_generator","notes_generator":"notes_generator","worksheet_generator":"worksheet_generator"}
    if tool not in allowed: abort(404)
    if request.method=="POST":
        module=importlib.import_module("ai."+allowed[tool]); content=module.generate(request.form.to_dict())
        title=request.form.get("title") or request.form.get("topic") or tool.replace("_"," ").title()
        doc=save_document(current_user.id,title,tool,content,request.form.to_dict())
        return redirect(url_for("editor",doc_id=doc.id))
    return render_template(f"{tool}.html",tool=tool)

@app.route("/workspace")
@login_required
def workspace():
    q=request.args.get("q","").strip()
    query=Document.query.filter_by(user_id=current_user.id)
    if q: query=query.filter(Document.title.ilike(f"%{q}%"))
    docs=query.order_by(Document.updated_at.desc()).all()
    return render_template("workspace.html",docs=docs,q=q)

@app.route("/editor/<int:doc_id>",methods=["GET","POST"])
@login_required
def editor(doc_id):
    doc=Document.query.filter_by(id=doc_id,user_id=current_user.id).first_or_404()
    if request.method=="POST":
        update_document(doc,request.form.get("title",doc.title),request.form.get("content",""))
        flash("Document saved.","success")
    return render_template("editor.html",doc=doc)

@app.post("/document/<int:doc_id>/delete")
@login_required
def delete_document(doc_id):
    doc=Document.query.filter_by(id=doc_id,user_id=current_user.id).first_or_404()
    db.session.delete(doc); db.session.commit(); flash("Deleted.","success")
    return redirect(url_for("workspace"))

@app.route("/document/<int:doc_id>/duplicate")
@login_required
def duplicate_document(doc_id):
    doc=Document.query.filter_by(id=doc_id,user_id=current_user.id).first_or_404()
    new=save_document(current_user.id,doc.title+" (Copy)",doc.tool,doc.content)
    return redirect(url_for("editor",doc_id=new.id))

@app.route("/document/<int:doc_id>/export/<fmt>")
@login_required
def export_document(doc_id,fmt):
    doc=Document.query.filter_by(id=doc_id,user_id=current_user.id).first_or_404()
    ext={"pdf":"pdf","docx":"docx","pptx":"pptx"}.get(fmt)
    if not ext: abort(404)
    path=os.path.join(app.config["EXPORT_FOLDER"],f"{doc.id}_{export_service.safe_name(doc.title)}.{ext}")
    if fmt=="pdf": export_service.export_pdf(doc.title,doc.content,path)
    elif fmt=="docx": export_service.export_docx(doc.title,doc.content,path)
    else: export_service.export_pptx(doc.title,doc.content,path)
    return send_file(path,as_attachment=True,download_name=os.path.basename(path))

@app.route("/analytics")
@login_required
def analytics(): return render_template("analytics.html",stats=user_analytics(current_user.id))

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin: abort(403)
    return render_template("admin.html",users=User.query.all(),documents=Document.query.order_by(Document.created_at.desc()).limit(30).all())

with app.app_context(): db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

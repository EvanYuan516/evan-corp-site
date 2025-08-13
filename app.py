from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# ------- 数据库配置 -------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭事件系统，省资源

db = SQLAlchemy(app)

# ------- 表模型（ORM） -------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)          # 自增主键
    name = db.Column(db.String(80), nullable=False)       # 姓名
    email = db.Column(db.String(120), nullable=False)     # 邮箱
    content = db.Column(db.Text, nullable=False)          # 留言内容（长文本）
    ip = db.Column(db.String(45))                         # 用户 IP（IPv6 兼容）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间（UTC）

    def __repr__(self):
        return f"<Message {self.id} {self.email}>"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
def products():
    product_list = [
        {
            "name": "无线耳机",
            "description": "高品质蓝牙耳机，支持降噪、触控操作",
            "image": "https://shopstatic.vivo.com.cn/vivoshop/commodity/commodity/10010967_1747138246443_750x750.png.webp"
        },
        {
            "name": "智能手表",
            "description": "支持心率监测、GPS 运动追踪、多语言系统",
            "image": "https://img.88tph.com/75/24/dSQKRd9PEe2RkAAWPgWqLw-1.jpg!/fw/700/watermark/url/L3BhdGgvbG9nby5wbmc/align/center"
        },
        {
            "name": "电动牙刷",
            "description": "USB 快充、防水设计、三档清洁模式",
            "image": "https://p1.lefile.cn/product/adminweb/2020/05/12/fDjIvRwCIAVbJKnkKJx3DJQqh-7610.jpg"
        }
    ]
    return render_template("products.html", products=product_list)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        content = (request.form.get("message") or "").strip()

        # 简单校验（快速兜底）
        if not name or not email or not content:
            return "字段不能为空", 400
        if "@" not in email:
            return "邮箱格式不正确", 400

        # 记录 IP（Nginx 反代时会带 X-Forwarded-For）
        ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)

        # 入库
        msg = Message(name=name, email=email, content=content, ip=ip_addr)
        db.session.add(msg)
        db.session.commit()

        # 处理完后跳转到一个“感谢页面”或原页面
        return redirect(url_for("thank_you"))    
    return render_template("contact.html")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/admin/messages")
def admin_messages():
    msgs = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("admin_messages.html", messages=msgs)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0", port=5000, debug=True)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
            "image": "https://via.placeholder.com/300x200?text=无线耳机"
        },
        {
            "name": "智能手表",
            "description": "支持心率监测、GPS 运动追踪、多语言系统",
            "image": "https://via.placeholder.com/300x200?text=智能手表"
        },
        {
            "name": "电动牙刷",
            "description": "USB 快充、防水设计、三档清洁模式",
            "image": "https://via.placeholder.com/300x200?text=电动牙刷"
        }
    ]
    return render_template("products.html", products=product_list)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # 先打印到终端，确认能收到
        print(f"姓名: {name}, 邮箱: {email}, 留言: {message}")

        # 处理完后跳转到一个“感谢页面”或原页面
        return redirect(url_for("thank_you"))    
    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
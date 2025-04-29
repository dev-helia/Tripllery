from quart import Quart
from quart_cors import cors

# 把三个蓝图都import进来！✨
from routes.recommend import recommend_bp
from routes.plan import plan_bp
from routes.preview import preview_bp  # 🆕 乖宝一定要补上这行！！

app = Quart(__name__)
app = cors(app, allow_origin="*")

# 注册所有蓝图！✨
app.register_blueprint(recommend_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(preview_bp)  # 🆕 乖宝补上这行！！

if __name__ == "__main__":
    app.run(debug=True, port=5001)

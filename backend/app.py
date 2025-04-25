from quart import Quart
from quart_cors import cors 
from routes.recommend import recommend_bp

app = Quart(__name__)
app = cors(app, allow_origin="*")  

app.register_blueprint(recommend_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

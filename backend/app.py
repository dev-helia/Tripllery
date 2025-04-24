from flask import Flask
from routes.recommend import recommend_bp 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(recommend_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

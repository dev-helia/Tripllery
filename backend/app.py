"""
app.py · Tripllery V3 Main Entry Point

This is the main startup script for the backend server.

Key Features:
-------------
✅ Based on Quart (async Flask-like framework)  
✅ CORS enabled (frontend-backend communication)  
✅ All three main API routes registered:
    - /recommend
    - /plan
    - /preview

Author: Tripllery AI Backend
"""

from quart import Quart
from quart_cors import cors

# ✅ Import all route blueprints
from routes.recommend import recommend_bp
from routes.plan import plan_bp
from routes.preview import preview_bp  # 🆕 Make sure this is included!

# Initialize app
app = Quart(__name__)
app = cors(app, allow_origin="*")  # Allow all origins for local frontend

# ✅ Register route blueprints
app.register_blueprint(recommend_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(preview_bp)  # 🆕 Required for /preview to work

# ✅ Launch server
if __name__ == "__main__":
    app.run(debug=True, port=5001)

from flask import Flask, jsonify
from api.dashboard import app as dashboard_app

app = Flask(__name__)

# Registrera blueprint från dashboard.py
app.register_blueprint(dashboard_app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

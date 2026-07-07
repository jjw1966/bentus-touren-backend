from flask import Flask, jsonify
from flask_cors import CORS

# Importera alla API-endpoints
from api.resultat import app as resultat_app
from api.tourstallning import app as tourstallning_app
from api.lagspel import app as lagspel_app
from api.deltavlingar import app as deltavlingar_app
from api.spelare import app as spelare_app
from api.dashboard import app as dashboard_app

app = Flask(__name__)
CORS(app)

# Registrera blueprints
app.register_blueprint(resultat_app)
app.register_blueprint(tourstallning_app)
app.register_blueprint(lagspel_app)
app.register_blueprint(deltavlingar_app)
app.register_blueprint(spelare_app)
app.register_blueprint(dashboard_app)

# Hem-route
@app.route("/")
def home():
    return jsonify({"status": "Bentus Touren Backend live 🎉"})

# Starta servern
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

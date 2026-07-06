from flask import Flask, jsonify
from flask_cors import CORS

from api.resultat import app as resultat_app
from api.tourstallning import app as tourstallning_app
from api.lagspel import app as lagspel_app
from api.deltavlingar import app as deltavlingar_app

app = Flask(__name__)
CORS(app)

app.register_blueprint(resultat_app)
app.register_blueprint(tourstallning_app)
app.register_blueprint(lagspel_app)
app.register_blueprint(deltavlingar_app)

@app.route("/")
def home():
    return jsonify({"status": "Backend live 🎉"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

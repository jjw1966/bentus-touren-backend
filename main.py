from flask import Flask
from flask_cors import CORS

from api.resultat import resultat_bp
from api.spelare import spelare_bp
from api.lagspel import lagspel_bp
from api.tourstallning import tourstallning_bp
from api.deltavlingar import deltavlingar_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(resultat_bp)
app.register_blueprint(spelare_bp)
app.register_blueprint(lagspel_bp)
app.register_blueprint(tourstallning_bp)
app.register_blueprint(deltavlingar_bp)

@app.route("/")
def home():
    return "Bentus Touren backend är igång!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

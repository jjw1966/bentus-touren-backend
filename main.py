from flask import Flask
from api.dashboard import app as dashboard_app
from api.spelare import app as spelare_app
from api.lagspel import app as lagspel_app
from api.tourstallning import app as tourstallning_app
from api.deltavlingar import app as deltavlingar_app

app = Flask(__name__)

# Registrera alla blueprints
app.register_blueprint(dashboard_app)
app.register_blueprint(spelare_app)
app.register_blueprint(lagspel_app)
app.register_blueprint(tourstallning_app)
app.register_blueprint(deltavlingar_app)

if __name__ == "__main__":
    print("Server running on port 10000...")
    app.run(host="0.0.0.0", port=10000)

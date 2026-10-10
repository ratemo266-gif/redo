import importlib

flask_module = importlib.import_module("flask")
Flask = flask_module.Flask

from routes import inventory_bp

app = Flask(__name__)
app.register_blueprint(inventory_bp)


if __name__ == "__main__":
    app.run(debug=True)
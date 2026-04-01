from flask import Flask
from routes.main import main_bp
from routes.puzzles import puzzles_bp

app = Flask(__name__)
app.secret_key = "super_secret_mission_key"

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(puzzles_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

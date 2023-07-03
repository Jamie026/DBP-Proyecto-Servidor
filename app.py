from flask import Flask
from flask_cors import CORS
from routes.user import users
from routes.group import groups
from routes.task import tasks
from models.db import db

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object("config.DevConfig")

db.init_app(app)
app.register_blueprint(users)
app.register_blueprint(groups)
app.register_blueprint(tasks)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="192.168.1.9", port=5000)
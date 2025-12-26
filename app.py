from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.task_routes import task_bp
from routes.comment_routes import comment_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    
    app.register_blueprint(task_bp)
    app.register_blueprint(comment_bp)
    
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

from flask import Flask
from extensions import db, bcrypt, login_manager
from routes.auth import auth_bp
from routes.tickets import tickets_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

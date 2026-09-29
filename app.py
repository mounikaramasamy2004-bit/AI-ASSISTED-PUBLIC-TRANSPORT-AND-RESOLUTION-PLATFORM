"""Flask application entry point.  Run with:  python app.py"""
import logging

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from config import Config
from database.database import db, init_db

jwt = JWTManager()
log = logging.getLogger("transport")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    jwt.init_app(app)
    init_db(app)

    from routes.admin_routes import admin_bp
    from routes.auth_routes import auth_bp
    from routes.chatbot_routes import chatbot_bp
    from routes.complaint_routes import complaint_bp
    from routes.route_routes import ai_bp, route_bp
    from routes.user_routes import user_bp
    from routes.vehicle_routes import vehicle_bp
    for bp in (auth_bp, user_bp, vehicle_bp, route_bp, ai_bp, complaint_bp, chatbot_bp, admin_bp):
        app.register_blueprint(bp)

    # ------------------------------------------------------------------ JWT errors (always 401 + JSON)
    from services import auth_service

    @jwt.token_in_blocklist_loader
    def _blocked(_header, payload):
        return payload["jti"] in auth_service.BLOCKLIST

    @jwt.unauthorized_loader
    def _missing(_reason):
        return jsonify({"success": False, "message": "Authentication required. Please log in."}), 401

    @jwt.invalid_token_loader
    def _invalid(_reason):
        return jsonify({"success": False, "message": "Invalid token. Please log in again."}), 401

    @jwt.expired_token_loader
    def _expired(_header, _payload):
        return jsonify({"success": False, "message": "Session expired. Please log in again."}), 401

    @jwt.revoked_token_loader
    def _revoked(_header, _payload):
        return jsonify({"success": False, "message": "You have been logged out."}), 401

    # ------------------------------------------------------------------ error handlers
    @app.errorhandler(HTTPException)
    def _http_error(e):
        messages = {400: "Bad request", 401: "Authentication required", 403: "Forbidden",
                    404: "Resource not found", 405: "Method not allowed"}
        return jsonify({"success": False, "message": messages.get(e.code, e.description)}), e.code

    @app.errorhandler(Exception)
    def _server_error(e):
        db.session.rollback()
        log.exception("Unhandled error")
        return jsonify({"success": False, "message": "Something went wrong on the server. Please try again."}), 500

    @app.get("/api/health")
    def health():
        return jsonify({"success": True, "status": "ok", "service": "AI Public Transport API"}), 200

    return app


def bootstrap(app):
    """Seed the database with demo data on first run."""
    from database.seed import seed_database
    with app.app_context():
        if seed_database():
            print("Database seeded with demo data.")
        from ai import delay_prediction
        print("Delay model trained:", delay_prediction.train())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    application = create_app()
    bootstrap(application)
    print("API running at http://127.0.0.1:5000/api  (health: /api/health)")
    application.run(host="127.0.0.1", port=5000, debug=False)

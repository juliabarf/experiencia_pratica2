# app/__init__.py

from flask import Flask, jsonify
from app.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return jsonify({
            "data": {
                "message": "Connect API esta no ar",
                "endpoints": {
                    "GET /users": "Lista todos os usuarios",
                    "POST /users": "Cria um novo usuario",
                    "GET /users/<id>": "Busca um usuario pelo ID",
                    "PUT /users/<id>": "Atualiza um usuario pelo ID",
                    "DELETE /users/<id>": "Remove um usuario pelo ID",
                }
            }
        }), 200

    return app

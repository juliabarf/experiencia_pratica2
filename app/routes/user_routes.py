# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from app.data.db import users, generate_id

user_bp = Blueprint("users", __name__, url_prefix="/users")


def validate_user_payload(data: dict, partial: bool = False) -> str | None:
    """
    Valida os campos essenciais do payload de usuario.
    Retorna uma mensagem de erro (str) caso alguma restricao seja violada,
    ou None caso os dados estejam integros.

    `partial=True` e usado em atualizacoes (PUT/PATCH), onde nem todos
    os campos precisam necessariamente estar presentes de uma vez -
    mas, se presentes, nao podem ser vazios ou de tipo invalido.
    """
    if not isinstance(data, dict) or not data:
        return "O corpo da requisicao deve ser um JSON valido e nao vazio"

    required_fields = ["name", "email"]

    if not partial:
        for field in required_fields:
            if field not in data:
                return f"O campo '{field}' e obrigatorio"

    for field in required_fields:
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not value.strip():
                return f"O campo '{field}' deve ser uma string nao vazia"

    if "email" in data and "@" not in data["email"]:
        return "O campo 'email' deve conter um endereco valido"

    return None


@user_bp.route("", methods=["GET"])
def get_users():
    """
    Recupera a colecao completa de usuarios.
    Nao requer corpo de requisicao.
    """
    return jsonify({"data": users}), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Recupera um unico usuario atraves do ID informado na URL.
    Trata explicitamente o cenario de ausencia do recurso (404).
    """
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuario nao encontrado"}), 404

    return jsonify({"data": user}), 200


@user_bp.route("", methods=["POST"])
def create_user():
    """
    Cria um novo usuario a partir do corpo da requisicao.
    Aplica validacao de entrada antes de manipular a estrutura em memoria.
    Envelope padronizado: {"data": ...} em sucesso, {"error": ...} em falha.
    """
    data = request.get_json(silent=True) or {}

    error_message = validate_user_payload(data)
    if error_message:
        return jsonify({"error": error_message}), 400

    new_user = {
        "id": generate_id(),
        "name": data["name"].strip(),
        "email": data["email"].strip(),
    }
    users.append(new_user)

    return jsonify({"data": new_user}), 201


@user_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    """
    Atualiza um usuario existente com os dados enviados no corpo da requisicao.
    Localiza o registro pelo ID; trata explicitamente o cenario de ausencia (404).
    Aplica a mesma validacao de entrada usada no cadastro.
    """
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuario nao encontrado"}), 404

    data = request.get_json(silent=True) or {}

    error_message = validate_user_payload(data, partial=True)
    if error_message:
        return jsonify({"error": error_message}), 400

    if "name" in data:
        user["name"] = data["name"].strip()
    if "email" in data:
        user["email"] = data["email"].strip()

    return jsonify({"data": user}), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Remove um usuario da estrutura em memoria.
    Localiza o registro pelo ID; trata explicitamente o cenario de ausencia (404).
    """
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuario nao encontrado"}), 404

    users.remove(user)

    return "", 204

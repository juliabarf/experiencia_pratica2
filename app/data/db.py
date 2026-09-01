# app/data/db.py

"""
Simulacao de banco de dados em memoria.
Os dados residem em RAM durante o ciclo de vida do processo Flask
e sao perdidos a cada reinicializacao do servidor.
"""

from itertools import count

# Estrutura de dados global que representa a "tabela" de usuarios
users: list[dict] = []

# Gerador de IDs incrementais (estrategia auto-increment)
_id_counter = count(1)


def generate_id() -> int:
    """Gera o proximo ID disponivel de forma incremental."""
    return next(_id_counter)

# utils/hash_evento.py

import hashlib

def gerar_hash_evento(titulo, descricao):

    texto = f"{titulo}-{descricao}"

    return hashlib.sha256(texto.encode("utf-8")).hexdigest()
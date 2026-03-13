import hashlib


def gerar_hash_evento(titulo, descricao, datas):

    texto = f"{titulo}-{descricao}-{datas}"

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()
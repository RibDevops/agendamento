import hashlib


def gerar_hash(evento):

    texto = f"""
    {evento['data']}
    {evento['titulo']}
    {evento['tipo']}
    {evento['descricao']}
    """

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()
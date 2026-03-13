import hashlib

from agenda.models import AgendaEvento


def gerar_hash_evento(evento):

    texto = f"""
    {evento.get('data')}
    {evento.get('titulo')}
    {evento.get('descricao')}
    """

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


def salvar_agenda(lista_eventos):

    salvos = 0
    ignorados = 0

    for evento in lista_eventos:

        hash_evento = gerar_hash_evento(evento)

        if AgendaEvento.objects.filter(hash=hash_evento).exists():

            ignorados += 1
            continue

        AgendaEvento.objects.create(

            data=evento.get("data"),

            dia=evento.get("dia"),

            titulo=evento.get("titulo"),

            tipo=evento.get("tipo"),

            datas=evento.get("datas"),

            descricao=evento.get("descricao"),

            hash=hash_evento
        )

        salvos += 1

    return {

        "salvos": salvos,
        "ignorados": ignorados
    }
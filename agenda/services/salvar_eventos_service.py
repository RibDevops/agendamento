from agenda.models import AgendaEvento
from agenda.utils.hash_evento import gerar_hash


def salvar_eventos(eventos):

    salvos = 0
    ignorados = 0

    for evento in eventos:

        hash_evento = gerar_hash(evento)

        if AgendaEvento.objects.filter(hash=hash_evento).exists():
            ignorados += 1
            continue

        AgendaEvento.objects.create(
            data=evento["data"],
            dia=evento["dia"],
            titulo=evento["titulo"],
            tipo=evento["tipo"],
            datas=evento["datas"],
            descricao=evento["descricao"],
            hash=hash_evento,
        )

        salvos += 1

    return {
        "salvos": salvos,
        "ignorados": ignorados
    }
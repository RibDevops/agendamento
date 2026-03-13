from .models import AgendaEvento
from .hash_utils import gerar_hash_evento


def salvar_eventos(eventos):

    novos_eventos = []

    for evento in eventos:

        hash_evento = gerar_hash_evento(
            evento["titulo"],
            evento["descricao"],
            evento["datas"]
        )

        obj, criado = AgendaEvento.objects.get_or_create(

            hash=hash_evento,

            defaults={

                "data": evento["data"],
                "dia": evento["dia"],
                "titulo": evento["titulo"],
                "tipo": evento["tipo"],
                "datas": evento["datas"],
                "descricao": evento["descricao"],
            }
        )

        if criado:

            novos_eventos.append(obj)

            print("Novo evento salvo:", obj.titulo)

    return novos_eventos
from agenda.models import AgendaEvento


def buscar_eventos_nao_enviados():

    eventos = AgendaEvento.objects.filter(
        enviado_whatsapp=False
    ).order_by("data")

    return eventos
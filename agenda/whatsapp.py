from .models import AgendaEvento


def enviar_whatsapp(mensagem):

    print("Enviando mensagem:")
    print(mensagem)

    # aqui você pode integrar com:
    # evolution api
    # z-api
    # wppconnect

def enviar_eventos_whatsapp():

    eventos = AgendaEvento.objects.filter(
        enviado_whatsapp=False
    )

    for evento in eventos:

        mensagem = f"""
📚 {evento.titulo}

📅 {evento.data}

📝 {evento.descricao[:200]}
"""

        enviar_whatsapp(mensagem)

        evento.enviado_whatsapp = True
        evento.save()
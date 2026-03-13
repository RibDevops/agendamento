def montar_mensagem(eventos):

    mensagem = "📚 *Agenda Escolar*\n\n"

    data_atual = None

    for evento in eventos:

        if data_atual != evento.data:

            data_atual = evento.data

            mensagem += f"\n📅 *{evento.data.strftime('%d/%m/%Y')}*\n"

        mensagem += f"""
📖 *{evento.titulo}*
Tipo: {evento.tipo}

{evento.descricao[:250]}...

------------------------
"""

    return mensagem
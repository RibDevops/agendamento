import time
import logging
import traceback

from agenda.models import AgendaEvento, Aluno, WhatsAppEnvio
from evolution.app import enviar_texto

logger = logging.getLogger(__name__)


def _montar_mensagem(evento):
    return (
        f"📚 *Nova atividade*\n\n"
        f"📌 *{evento.titulo}*\n"
        f"📂 Tipo: {evento.tipo}\n"
        f"🗓 Data: {evento.data.strftime('%d/%m/%Y')}\n\n"
        f"{evento.descricao}"
    )


def enviar_tarefas():

    logger.info("📲 Iniciando envio WhatsApp")

    eventos = AgendaEvento.objects.filter(enviado_whatsapp=False).order_by("data")

    logger.info(f"📋 Eventos pendentes de envio: {eventos.count()}")

    for evento in eventos:

        turma = evento.turma

        # ---------------------------------------------------
        # Verifica se já foi enviado para essa turma
        # ---------------------------------------------------

        ja_enviado = WhatsAppEnvio.objects.filter(
            turma=turma,
            hash_evento=evento.hash
        ).exists()

        if ja_enviado:
            logger.info(f"⚠ Evento '{evento.titulo}' já enviado para turma {turma}. Ignorando.")
            evento.enviado_whatsapp = True
            evento.save(update_fields=["enviado_whatsapp"])
            continue

        if turma is None:
            logger.warning(f"⚠ Evento '{evento.titulo}' sem turma associada. Ignorando.")
            continue

        alunos = Aluno.objects.filter(turma=turma)

        if not alunos.exists():
            logger.warning(f"⚠ Nenhum aluno na turma {turma}. Ignorando evento '{evento.titulo}'.")
            continue

        mensagem = _montar_mensagem(evento)

        logger.info(f"📤 Enviando '{evento.titulo}' para turma {turma} ({alunos.count()} aluno(s))")

        algum_enviado = False

        for aluno in alunos:

            numero = aluno.telefone

            if not numero:
                logger.warning(f"⚠ Aluno '{aluno.nome_aluno}' sem telefone. Pulando.")
                continue

            try:

                response = enviar_texto(numero, mensagem)

                if response.status_code in [200, 201]:
                    logger.info(f"✅ Enviado para {aluno.nome_aluno} ({numero})")
                    algum_enviado = True
                    time.sleep(4)

                else:
                    logger.warning(f"⚠ Resposta inesperada para {numero}: {response.status_code}")

            except Exception as e:
                logger.error(f"❌ Erro ao enviar para {numero}: {e}")
                traceback.print_exc()

        # ---------------------------------------------------
        # Registra envio por turma + hash (evita duplicidade)
        # ---------------------------------------------------

        if algum_enviado:

            WhatsAppEnvio.objects.get_or_create(
                turma=turma,
                hash_evento=evento.hash
            )

            logger.info(f"📝 Envio registrado — turma: {turma} | hash: {evento.hash[:12]}...")

        evento.enviado_whatsapp = True
        evento.save(update_fields=["enviado_whatsapp"])

    logger.info("✅ Envio finalizado")

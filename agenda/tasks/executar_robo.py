import os
import sys
import django

# caminho da raiz do projeto
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

django.setup()

from agenda.robots.agenda_robot import extrair_eventos
from agenda.services.salvar_eventos_service import salvar_eventos
from agenda.services.envio_service import enviar_tarefas


def executar():

    print("🚀 Iniciando robô...")

    eventos = extrair_eventos()

    print("Eventos encontrados:", len(eventos))

    resultado = salvar_eventos(eventos)

    print("\nResultado:")

    print("Eventos salvos:", resultado["salvos"])

    print("Eventos ignorados:", resultado["ignorados"])

    print("\n📲 Enviando WhatsApp...")

    enviar_tarefas()

    print("Envio finalizado")


if __name__ == "__main__":

    executar()
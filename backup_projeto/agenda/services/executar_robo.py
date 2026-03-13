import os
import sys
import django

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

django.setup()

from agenda.scraper import extrair_eventos
from agenda.views.views_salvar import salvar_agenda
#/home/suporte/Documentos/dev/dever/agenda/views/views_salvar.py

def executar():

    print("Iniciando robô...")

    eventos = extrair_eventos()

    print("Eventos encontrados:", len(eventos))

    resultado = salvar_agenda(eventos)

    print("\nResultado:")

    print("Eventos salvos:", resultado["salvos"])

    print("Eventos ignorados:", resultado["ignorados"])


if __name__ == "__main__":

    executar()
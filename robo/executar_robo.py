import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from agenda.scraper import extrair_eventos


def executar():

    print("Iniciando robô...")

    eventos = extrair_eventos()

    print("Eventos encontrados:", len(eventos))

    for e in eventos:
        print(e)


if __name__ == "__main__":
    executar()
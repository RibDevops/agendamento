from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re

def extrair_eventos():

    dados = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://mb4.bernoulli.com.br/login")

        # LOGIN
        page.get_by_role("textbox", name="Login").fill("cecilia.amaro@soulasalle.com.br")
        page.get_by_role("textbox", name="Senha").fill("#30Ceci3004")

        page.get_by_role("button", name="ENTRAR").click()
        page.get_by_role("button", name="AVANÇAR").click()

        page.locator("div").filter(has_text="Que bom ter você aqui no Meu").nth(1).click()
        page.get_by_role("button").nth(1).click()

        # IR PARA AGENDA
        page.goto("https://mb4.bernoulli.com.br/minhaarea/agenda")

        page.wait_for_selector(".calendario-table-days")

        semanas = page.query_selector_all(".calendario-table-days .semana")

        hoje = datetime.now().date()
        limite = hoje + timedelta(days=3)

        for semana in semanas:

            dias = semana.query_selector_all(".semana-day")

            for dia in dias:

                data_iso = dia.get_attribute("data-date")

                if not data_iso:
                    continue

                data = datetime.fromisoformat(data_iso.replace("Z", ""))

                # FILTRO DE DATA
                if not (hoje <= data.date() <= limite):
                    continue

                numero_dia = dia.query_selector(".day").inner_text()

                eventos = dia.query_selector_all(".tag-circle")

                if not eventos:
                    continue

                page.locator("a").filter(has_text=numero_dia).first.click()

                page.wait_for_selector(".EventItem")

                lista_eventos = page.locator(".EventItem")

                total = lista_eventos.count()

                for i in range(total):

                    evento = lista_eventos.nth(i)

                    nome = evento.locator(".eventName span").nth(1).inner_text()

                    evento.click()

                    modal = page.locator(".ModalContent.Event")
                    modal.wait_for()

                    titulo = modal.locator(".title-24-600").inner_text()

                    tipo = modal.locator(".Tag span").inner_text()

                    datas = modal.locator(".ph-calendar").locator("xpath=..").inner_text()

                    descricao = modal.locator(".event-description").inner_text()

                    # ARQUIVOS
                    arquivos = []

                    downloads = modal.locator(".FileDownload")

                    qtd = downloads.count()

                    for j in range(qtd):

                        item = downloads.nth(j)

                        nome_arquivo = item.inner_text()

                        link = item.locator("a").get_attribute("href")

                        arquivos.append({
                            "nome": nome_arquivo,
                            "link": link
                        })

                    dados.append({

                        "data": data.date(),
                        "dia": numero_dia,
                        "titulo": titulo,
                        "tipo": tipo,
                        "datas": datas,
                        "descricao": descricao,
                        "arquivos": arquivos

                    })

                    # FECHAR MODAL
                    page.get_by_role("button").filter(
                        has_text=re.compile(r"^$")
                    ).nth(4).click()

                    page.wait_for_timeout(500)

        browser.close()

    return dados


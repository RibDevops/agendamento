import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mb4.bernoulli.com.br/login")
    page.get_by_role("textbox", name="Login").click()
    page.get_by_role("textbox", name="Login").fill("cecilia.amaro@soulasalle.com.br")
    page.get_by_role("textbox", name="Senha").click()
    page.get_by_role("textbox", name="Senha").fill("#30Ceci3004")
    page.get_by_role("button", name="ENTRAR").click()
    page.get_by_role("button", name="AVANÇAR").click()
    page.goto("https://mb4.bernoulli.com.br/")
    page.locator("div").filter(has_text="Que bom ter você aqui no Meu").nth(1).click()
    page.get_by_role("button").nth(2).click()
    page.get_by_role("button", name=" Minha Área").click()
    page.get_by_role("button", name=" Agenda").click()
    page.get_by_text("CalendárioListaPainel").click()
    page.get_by_role("button", name="Calendário").click()
    page.get_by_text("terça-feira14 de abrilDever").click()
    page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(3).click()
    page.locator("div").filter(has_text=re.compile(r"^Dever de sala e de casa$")).nth(1).click()
    page.get_by_text("Dever de sala e de casaTarefa10/03/26, 10:50 à 31/12/26, 23:59Dever de sala:").click()
    page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(3).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

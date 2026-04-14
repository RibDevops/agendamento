import os
import json
import time
import random
import logging
import traceback
from datetime import datetime
from playwright.sync_api import sync_playwright

# -------------------------------------------------------------------------
# 1. CONFIGURAÇÕES INICIAIS E LOGGING
# -------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Onde os cookies de sessão serão salvos para evitar logins repetidos
COOKIES_PATH = "agenda/storage/cookies.json"
# Onde os dados finais da agenda serão salvos (simulando um dump ou preparação para o Django)
DADOS_SAIDA_PATH = "agenda/storage/agenda_extraida.json"

os.makedirs(os.path.dirname(COOKIES_PATH), exist_ok=True)

# -------------------------------------------------------------------------
# 2. FUNÇÕES DE UTILIDADE E SESSÃO
# -------------------------------------------------------------------------

def carregar_cookies(context):
    """Carrega cookies salvos para tentar reaproveitar a sessão."""
    if os.path.exists(COOKIES_PATH):
        try:
            with open(COOKIES_PATH, "r") as f:
                cookies = json.load(f)
            context.add_cookies(cookies)
            logger.info("🍪 Cookies carregados com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar cookies: {e}")
    return False

def salvar_cookies(context):
    """Salva os cookies atuais após um login bem-sucedido."""
    cookies = context.cookies()
    with open(COOKIES_PATH, "w") as f:
        json.dump(cookies, f)
    logger.info("💾 Cookies de sessão salvos.")

def delay():
    """Simula comportamento humano com pausas aleatórias."""
    time.sleep(random.uniform(1.5, 3.0))

# -------------------------------------------------------------------------
# 3. LÓGICA DE NAVEGAÇÃO E LOGIN
# -------------------------------------------------------------------------

def realizar_login(page, context, login, senha):
    """Executa o fluxo de login usando seletores estáveis."""
    logger.info("🔗 Acessando página de login...")
    page.goto("https://mb4.bernoulli.com.br/login")

    # Usando get_by_role para maior estabilidade (visto no seu robo_simples)
    page.get_by_role("textbox", name="Login").fill(login)
    page.get_by_role("textbox", name="Senha").fill(senha)
    
    delay()
    page.get_by_role("button", name="ENTRAR").click()

    # Lida com o botão 'AVANÇAR' que aparece após o login
    try:
        page.get_by_role("button", name="AVANÇAR").wait_for(timeout=10000)
        page.get_by_role("button", name="AVANÇAR").click()
        logger.info("✅ Login efetuado e botão AVANÇAR clicado.")
    except:
        logger.info("ℹ️ Botão AVANÇAR não detectado (pode já estar logado).")

    # Aguarda o carregamento da URL principal para garantir que o Token JWT foi gerado
    page.wait_for_url("**/minhaarea**", timeout=15000)
    salvar_cookies(context)

# -------------------------------------------------------------------------
# 4. EXTRAÇÃO VIA API (O "PULO DO GATO")
# -------------------------------------------------------------------------

def extrair_agenda_via_api(page):
    """
    Usa o Burp Suite Insight: faz o fetch direto no endpoint da API
    dentro do contexto do navegador logado.
    """
    logger.info("🛰️ Solicitando dados para a API interna...")
    
    # Datas de exemplo baseadas no seu log do Burp
    data_inicio = "2026-03-07"
    data_fim = "2026-05-22"
    url_api = f"https://api.bernoulli.com.br/api/comunicacao/agenda/listar?dataInicio={data_inicio}&dataTermino={data_fim}"

    # O evaluate executa JavaScript dentro da página, herdando o cabeçalho 'Authorization'
    # que o navegador já possui por estar logado.
    script_js = f"""
        async () => {{
            const resp = await fetch('{url_api}', {{
                method: 'GET',
                headers: {{
                    'Accept': 'application/json',
                    'Front-Version': '4.25.50',
                    'Plataforma': '2'
                }}
            }});
            return await resp.json();
        }}
    """
    
    try:
        resultado = page.evaluate(script_js)
        # Onde os dados estão sendo "salvos" temporariamente: na variável 'eventos'
        eventos = resultado.get('data', [])
        logger.info(f"📊 {len(eventos)} eventos encontrados na API.")
        return eventos
    except Exception as e:
        logger.error(f"Erro ao consultar API: {e}")
        return []

# -------------------------------------------------------------------------
# 5. SALVAMENTO DOS DADOS (BANCO DE DADOS / ARQUIVO)
# -------------------------------------------------------------------------

def salvar_dados_finais(dados):
    """
    Aqui é onde os dados são persistidos.
    COMENTÁRIO: No seu caso, você deve substituir a escrita do JSON 
    pela chamada do seu Model Django (ex: Agenda.objects.create(...))
    """
    if not dados:
        logger.warning("⚠️ Nenhum dado para salvar.")
        return

    # SALVAMENTO EM ARQUIVO (LOCAL)
    # Útil para debug ou para o seu script de 'sincronizar_agenda' ler depois
    with open(DADOS_SAIDA_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    
    logger.info(f"💾 DADOS SALVOS EM: {DADOS_SAIDA_PATH}")

    # EXEMPLO DE COMO SERIA PARA O DJANGO:
    # for item in dados:
    #     Agenda.objects.update_or_create(
    #         external_id=item['id'],
    #         defaults={'titulo': item['titulo'], 'data': item['dataInicio']}
    #     )

# -------------------------------------------------------------------------
# 6. EXECUÇÃO PRINCIPAL
# -------------------------------------------------------------------------

def executar_robo(login, senha):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Mude para True em produção
        context = browser.new_context()
        
        # Tenta reaproveitar sessão
        sessao_ativa = carregar_cookies(context)
        page = context.new_page()

        try:
            # Se não tiver cookies ou a página de login aparecer, faz o login
            page.goto("https://mb4.bernoulli.com.br/minhaarea")
            if "login" in page.url:
                realizar_login(page, context, login, senha)
            
            # Extração
            agenda_dados = extrair_agenda_via_api(page)
            
            # Salvamento (Onde os dados são persistidos)
            salvar_dados_finais(agenda_dados)

        except Exception as e:
            logger.error(f"Erro crítico: {e}")
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    # Credenciais (Idealmente usar variáveis de ambiente ou .env)
    USER = "cecilia.amaro@soulasalle.com.br"
    PASS = "#30Ceci3004"
    
    executar_robo(USER, PASS)
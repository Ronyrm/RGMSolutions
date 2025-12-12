from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

FILTERS = {
    "dyMin": "7",
    "dyMax": "14",
    "pvpMin": "0.80",
    "pvpMax": "1.05",
    "liquidezMin": "1000000",
    "liquidezMax": "5000000",
    "marketcapMin": "500000000",
    "marketcapMax": "10000000000"
}

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://statusinvest.com.br/fundos-imobiliarios/busca-avancada")

wait = WebDriverWait(driver, 20)

# 🔥 Tentar fechar propaganda
try:
    ad_close = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, "button[id*='close'], .close, .btn-close")))
    ad_close.click()
    print("Popup fechado.")
    time.sleep(1)
except:
    print("Nenhum popup detectado.")

# 🔥 ROLAR PARA OS CAMPOS
driver.execute_script("window.scrollTo(0, 800);")
time.sleep(2)


def fill_by_name(name, value):
    print("Iniciando buscas por "+name+"|valor: "+value)
    element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='{name}']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.3)

    # LIMPAR VIA JS (send_keys não funciona nesses inputs)
    driver.execute_script("arguments[0].value='';", element)
    time.sleep(0.2)

    # DEFINIR VALOR VIA JS
    driver.execute_script("arguments[0].value=arguments[1];", element, value)
    time.sleep(0.3)


def fill_input(css_selector, value):
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(0.3)
    element.clear()
    element.send_keys(value)
    time.sleep(0.4)

# 🔥 PREENCHER FILTROS
fill_by_name("dy|0", FILTERS["dyMin"])
fill_by_name("dy|1", FILTERS["dyMax"])

# 🔥 CLICAR BUSCAR
btn_buscar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Buscar')]"))
)

# 1. Scroll controlado para evitar ficar sob o header
driver.execute_script("""
    const y = arguments[0].getBoundingClientRect().top + window.pageYOffset - 150;
    window.scrollTo({top: y});
""", btn_buscar)

time.sleep(1)

# 2. Remove temporariamente a navbar fixa que está atrapalhando
driver.execute_script("""
    const nav = document.querySelector('.navbar-wrapper');
    if (nav) nav.style.display = 'none';
""")

time.sleep(0.5)

# 3. Tenta clique normal, senão força via JS
try:
    btn_buscar.click()
except:
    driver.execute_script("arguments[0].click();", btn_buscar)

time.sleep(4)

# 1️⃣ Abre o dropdown
dropdown = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.select-dropdown"))
)

# 1 — Garantir que está visível
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
time.sleep(0.5)

# 2 — Empurrar a página pra baixo para fugir da topbar
driver.execute_script("window.scrollBy(0, 200);")
time.sleep(0.3)

# 3 — Clicar via JS para ignorar elemento sobreposto
driver.execute_script("arguments[0].click();", dropdown)
time.sleep(0.5)

# 2️⃣ Acha o UL da lista
ul_id = dropdown.get_attribute("data-target")
ul_selector = f"ul#{ul_id} li span"

# 3️⃣ Procura o item "Todos" dentro do dropdown
opcoes = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ul_selector))
)

for opcao in opcoes:
    if "Todos" in opcao.text:
        opcao.click()
        break

time.sleep(1)

# 🔥 EXPORTAR CSV
btn_download = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn-download"))
)

# 1 — Rola a página para garantir que o botão está no meio da tela
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_download)
time.sleep(0.5)

# 2 — Dá um pequeno scroll pra baixo (evita topbar sobrepondo)
driver.execute_script("window.scrollBy(0, 200);")
time.sleep(0.3)

# 3 — Clicar via JavaScript (100% funciona)
driver.execute_script("arguments[0].click();", btn_download)
time.sleep(1)

print("✔ Download solicitado!")

time.sleep(20)
driver.quit()

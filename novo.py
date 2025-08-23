import time
import random
import traceback
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

import config
from utils import setup_logger, send_google_chat_notification

logger = setup_logger()

def highlight(element, driver):
    """Destaca um elemento na tela com uma borda amarela."""
    driver.execute_script("arguments[0].style.border='3px solid yellow'", element)
    time.sleep(1)

def setup_browser():
    """Configura o navegador Chrome com opções anti-bot."""
    chrome_options = Options()
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]
    random_user_agent = random.choice(user_agents)
    logger.info(f"Usando User-Agent: {random_user_agent}")
    chrome_options.add_argument(f"user-agent={random_user_agent}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def perform_scraping():
    """Executa o roteiro de scraping passo a passo."""
    driver = setup_browser()
    
    try:
        logger.info("Acessando a página de login...")
        driver.get(config.LOGIN_URL)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-mask"))).send_keys(config.USERNAME)
        driver.find_element(By.ID, "mod-login-password").send_keys(config.PASSWORD)
        driver.find_element(By.ID, "botao").click()
        WebDriverWait(driver, 20).until(EC.url_contains("principal.xhtml"))
        fiscalizacao_xpath = "//span[text()='Fiscalização']"
        fiscalizacao_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, fiscalizacao_xpath)))
        ActionChains(driver).move_to_element(fiscalizacao_element).perform()
        espaco_nip_xpath = "//span[text()='Espaço NIP']"
        espaco_nip_element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, espaco_nip_xpath)))
        espaco_nip_element.click()
        WebDriverWait(driver, 15).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "frameConteudoDialog")))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "formContent:j_idt85:abaContraOperadora")))
        em_andamento_link_xpath = "//a[contains(@href, 'abaContraOperadora')]"
        em_andamento_element = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, em_andamento_link_xpath)))
        em_andamento_element.click()
        time.sleep(random.uniform(2, 4)) 

        logger.info("Coletando os dados da tabela...")
        table_id = "formContent:j_idt85:tbDemandaEmAndamento"
        table_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, table_id)))
        headers = [header.text.strip() for header in table_element.find_elements(By.XPATH, ".//thead/tr/th/span")]
        logger.info(f"Colunas encontradas: {headers}")
        rows = table_element.find_elements(By.XPATH, ".//tbody/tr")
        
        json_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = []
            for cell in cells:
                cell_text = driver.execute_script("return arguments[0].innerText;", cell).strip().replace('\n', ' ')
                row_data.append(cell_text)
            row_dict = dict(zip(headers, row_data))
            json_data.append(row_dict)
        
        logger.info(f"Total de {len(json_data)} registros encontrados para salvar em JSON.")
        
        json_path = os.path.join(config.DOWNLOAD_PATH, "dados_nip.json")
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        logger.info(f"Dados salvos com sucesso em: {json_path}")

        if json_data:
            chat_message_header = f"✅ Encontradas {len(json_data)} novas demandas na ANS!\n\n"
            chat_message_body = ""
            records_to_send = json_data[:10]
            for record in records_to_send:
                demanda = record.get("Demanda", "N/A")
                protocolo = record.get("Protocolo", "N/A")
                status_atual = record.get("Status Atual", "N/A")
                data_notificacao = record.get("Data da Notificação", "N/A")
                chat_message_body += (
                    f"--------------\n"
                    f"Data: {data_notificacao}\n"
                    f"Demanda: {demanda}\n"
                    f"Protocolo: {protocolo}\n"
                    f"Status: {status_atual}\n"
                )
            if len(json_data) > 10:
                chat_message_body += f"\n...\n(Exibindo apenas os primeiros 10 registros. Verifique o arquivo JSON para todos os {len(json_data)} registros.)"
            
            send_google_chat_notification(chat_message_header + chat_message_body)
        else:
            send_google_chat_notification("✅ Nenhuma nova demanda encontrada na ANS.")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        error_message = f"❌ Ocorreu um erro durante o scraping da ANS.\n\nDetalhes do erro:\n{e}"
        send_google_chat_notification(error_message, is_error=True)
        logger.error(traceback.format_exc())

    finally:
        logger.info("Fechando o navegador.")
        driver.quit()

if __name__ == "__main__":
    perform_scraping()
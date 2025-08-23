import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def coletar_dados_tabela():
    """
    Função completa para inicializar o navegador, fazer o login,
    coletar os dados de uma tabela e retornar os dados em formato de lista de dicionários.
    """
    print("Iniciando o processo de coleta de dados...")

    # --- Configurações do WebDriver ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa em modo headless (sem interface gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use o User-Agent para evitar detecção
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    # Inicializa o WebDriver
    service = Service(executable_path="/usr/bin/chromedriver") # Caminho para o driver no Coolify/Linux
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Driver Chrome inicializado com sucesso.")

    try:
        # --- Acesso e Login (Exemplo) ---
        print("Acessando a página de login...")
        # driver.get("http://192.168.40.25:8000/login") # Substitua pela sua URL
        # time.sleep(5)  # Espera o carregamento da página

        # # Exemplo de preenchimento de login (ajuste para o seu caso)
        # driver.find_element(By.ID, "username").send_keys("seu_usuario")
        # driver.find_element(By.ID, "password").send_keys("sua_senha")
        # driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # time.sleep(10) # Espera o login e o redirecionamento

        # --- Coleta dos Dados da Tabela ---
        print("Coletando os dados da tabela...")
        tabela = driver.find_element(By.CSS_SELECTOR, "table.table") # Ajuste o seletor da sua tabela

        # Coleta os cabeçalhos da tabela
        headers = [th.text for th in tabela.find_elements(By.TAG_NAME, "th")]
        print(f"Colunas encontradas: {headers}")

        # Coleta os dados das linhas
        rows_data = []
        for tr in tabela.find_elements(By.TAG_NAME, "tr")[1:]: # Ignora a primeira linha (cabeçalho)
            cells = tr.find_elements(By.TAG_NAME, "td")
            if cells:
                row_values = [cell.text for cell in cells]
                rows_data.append(dict(zip(headers, row_values)))

        print(f"Total de {len(rows_data)} registros coletados.")
        return rows_data

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None  # Retorna None em caso de falha

    finally:
        # Garante que o navegador seja fechado, mesmo em caso de erro
        print("Fechando o navegador.")
        driver.quit()

# --- Exemplo de como usar a função ---
if __name__ == "__main__":
    dados = coletar_dados_tabela()
    if dados:
        # Agora você pode usar a variável 'dados' como uma lista de dicionários
        # Exemplo: print(dados)
        
        # Para salvar em um arquivo JSON (apenas para teste local)
        # with open('dados.json', 'w', encoding='utf-8') as f:
        #    json.dump(dados, f, indent=4, ensure_ascii=False)
        print("\nDados coletados com sucesso. Você pode processá-los aqui.")
        
    else:
        print("\nFalha na coleta de dados.")

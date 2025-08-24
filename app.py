from flask import Flask
import threading
import time
import novo # Importe seu script de scraping

app = Flask(__name__)

def job():
    """Função que executa o scraping e espera."""
    while True:
        try:
            print("Executando scraping...")
            novo.perform_scraping()
            
            # Gera um tempo de espera aleatório entre 6 e 8 horas
            random_sleep_time = random.randint(6 * 3600, 8 * 3600)
            print(f"Scraping concluído. Aguardando {random_sleep_time // 3600} horas e {(random_sleep_time % 3600) // 60} minutos...")
            time.sleep(random_sleep_time) 
        except Exception as e:
            print(f"Ocorreu um erro durante o scraping: {e}")
            # Em caso de erro, espera 1 minuto para tentar novamente
            time.sleep(60)

threading.Thread(target=job, daemon=True).start()

@app.route("/")
def home():
    return "Serviço de scraping ativo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

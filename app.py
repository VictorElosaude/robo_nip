from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import novo
import atexit
import logging

app = Flask(__name__)

# Configura o logger do Flask para não duplicar logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def job():
    """Função que executa o script de scraping."""
    novo.perform_scraping()

# Cria o agendador de tarefas
scheduler = BackgroundScheduler()

# Adiciona a tarefa de scraping para rodar a cada 5 minutos
scheduler.add_job(func=job, trigger='interval', minutes=5)

# Inicia o agendador
scheduler.start()

# Garante que o agendador seja desligado corretamente ao sair do aplicativo
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def home():
    """Rota principal que confirma que o serviço está no ar."""
    return "Serviço de scraping em andamento!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

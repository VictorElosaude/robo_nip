from flask import Flask
import threading
import time

app = Flask(__name__)

def job():
    while True:
        print("Executando job...")
        time.sleep(300)  # executa a cada 5 minutos

threading.Thread(target=job).start()

@app.route("/")
def home():
    return "Serviço rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

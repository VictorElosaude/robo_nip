# utils.py

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import requests
import json
import os

from config import GOOGLE_CHAT_WEBHOOK_URL, GOOGLE_CHAT_LOGO_URL

# Configuração do caminho do arquivo de log diário
LOG_FILE_PATH = f"logs/ans_monitor_{datetime.now().strftime('%Y-%m-%d')}.log"

def setup_logger():
    """Configura um logger para o sistema, com saída para console e arquivo."""
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        log_dir = os.path.dirname(LOG_FILE_PATH)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    return logger

logger = setup_logger()

def send_google_chat_notification(message_text, is_error=False, log_file_path=None):
    """
    Envia uma mensagem formatada com cartão para o Google Chat.
    """
    if not GOOGLE_CHAT_WEBHOOK_URL:
        logger.error("URL do Webhook do Google Chat não configurada.")
        return False

    if is_error:
        title = "❌ ERRO no Processo de Scraping"
        header_text = "Setor de Inovação Informa: Falha no processo"
    else:
        title = "✅ Processo de Scraping Concluído"
        header_text = "Setor de Inovação Informa:"

    full_message = message_text
    if log_file_path and os.path.exists(log_file_path):
        try:
            with open(log_file_path, "r", encoding='utf-8') as f:
                log_content = f.read()
            full_message += f"\n\n--- LOG COMPLETO ---\n```\n{log_content}\n```"
        except Exception as e:
            logger.error(f"Erro ao ler arquivo de log: {e}")

    chat_message = {
        "cardsV2": [
            {
                "cardId": "card_id_1",
                "card": {
                    "header": {
                        "title": header_text,
                        "subtitle": title,
                        "imageUrl": GOOGLE_CHAT_LOGO_URL
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": full_message
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }

    try:
        response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=chat_message, timeout=15)
        response.raise_for_status()
        logger.info(f"Notificação do Google Chat enviada com status HTTP {response.status_code}.")
        return True
    except requests.exceptions.RequestException as e:
        logger.critical(f"Falha ao enviar notificação: {e}.")
        return False
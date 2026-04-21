import requests
import os
import logging
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

class Reporter:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    def format_as_table(self, data_list):
        if not data_list or not isinstance(data_list, list):
            return "Nessun dato disponibile."

        headers = ["Partita", "Quota", "Consiglio AI", "Analisi"]
        table_data = []

        for item in data_list:
            # Shorten the analysis to fit better in mobile view if possible
            analisi = item.get('Analisi_Tecnica', '')
            if len(analisi) > 100:
                analisi = analisi[:97] + "..."

            table_data.append([
                item.get('Partita', 'N/D'),
                item.get('Quota_Eurobet', 'N/D'),
                item.get('Giocata_Suggerita', 'N/D'),
                analisi
            ])

        return tabulate(table_data, headers=headers, tablefmt="simple")

    def send_to_telegram(self, data, caption="📊 Analisi premium del weekend pronta!"):
        if not self.telegram_token or not self.chat_id:
            logging.error("Telegram Token o Chat ID non configurati")
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        
        try:
            table_html = self.format_as_table(data)
            message_text = f"{caption}\n\n<pre>{table_html}</pre>"

            data_req = {
                "chat_id": self.chat_id,
                "text": message_text,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data_req)

            if response.status_code == 200:
                logging.info("Messaggio inviato correttamente su Telegram.")
                return True
            else:
                logging.error(f"Errore invio Telegram: {response.text}")
                return False
        except Exception as e:
            logging.error(f"Errore durante l'invio Telegram: {e}")
            return False

if __name__ == "__main__":
    pass

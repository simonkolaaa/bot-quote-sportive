import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Reporter:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    def generate_excel(self, data_list, filename="Top_Giocate_Weekend.xlsx"):
        if not data_list:
            print("⚠️ Nessun dato da inserire nell'Excel.")
            return None
            
        df = pd.DataFrame(data_list)
        
        # Riordina le colonne se presenti
        standard_order = [
            "Campionato", "Squadra_Casa", "Squadra_Trasferta", 
            "Quota_Eurobet", "Affidabilita_1_10", 
            "Giocata_Suggerita", "Consiglio_Pengwin", "Analisi_Tecnica"
        ]
        
        # Filtra solo le colonne effettivamente presenti nei dati
        existing_cols = [c for c in standard_order if c in df.columns]
        other_cols = [c for c in df.columns if c not in standard_order]
        df = df[existing_cols + other_cols]

        try:
            df.to_excel(filename, index=False)
            print(f"✅ Report Excel generato con successo: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Errore nella generazione Excel: {e}")
            return None

    def send_to_telegram(self, file_path, caption="📊 Analisi premium del weekend pronta!"):
        if not self.telegram_token or not self.chat_id:
            print("Telegram Token o Chat ID non configurati")
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendDocument"
        
        try:
            with open(file_path, "rb") as file:
                files = {"document": file}
                data = {"chat_id": self.chat_id, "caption": caption}
                response = requests.post(url, files=files, data=data)
                
                if response.status_code == 200:
                    print("File inviato correttamente su Telegram.")
                    return True
                else:
                    print(f"Errore invio Telegram: {response.text}")
                    return False
        except Exception as e:
            print(f"Errore durante l'invio Telegram: {e}")
            return False

if __name__ == "__main__":
    # Test
    # reporter = Reporter()
    # reporter.generate_excel([{"Test": "Successo"}])
    pass

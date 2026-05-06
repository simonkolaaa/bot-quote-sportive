import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AIAnalyst:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def analyze_matches(self, matches_data):
        if not self.model:
            return {"error": "Gemini API Key non configurata"}

        if not matches_data:
            print("⚠️ Nessun dato ricevuto per l'analisi AI.")
            return []

        prompt = f"""
        Agisci da analista betting professionista. Ti fornirò una lista di partite con quote e statistiche.
        Dati:
        {json.dumps(matches_data, indent=2)}

        Obiettivo:
        Filtra il rumore e seleziona SOLO le 3-5 partite con il valore più alto (Value Bet).
        Per ogni partita scelta, fornisci un'analisi dettagliata.

        Restituiscimi un file JSON rigoroso (senza testo extra) con questa struttura:
        [
          {{
            "Campionato": "Nome Campionato",
            "Squadra_Casa": "Nome Squadra Casa",
            "Squadra_Trasferta": "Nome Squadra Trasferta",
            "Quota_Eurobet": "Es: 1.85",
            "Consiglio_Pengwin": "Il pronostico base",
            "Giocata_Suggerita": "La tua giocata definitiva",
            "Analisi_Tecnica": "Motivazione tecnica basata sui dati di forma e quote",
            "Affidabilita_1_10": "Voto da 1 a 10"
          }}
        ]
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON from potential markdown backticks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            cleaned_text = text.strip()
            if not cleaned_text:
                return []
                
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"❌ Errore durante l'analisi AI: {str(e)}")
            return {"error": f"Errore durante l'analisi AI: {str(e)}"}

if __name__ == "__main__":
    # Test
    analyst = AIAnalyst()
    # print(analyst.analyze_matches([]))

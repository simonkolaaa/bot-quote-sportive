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
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None

    def analyze_matches(self, matches_data):
        if not self.model:
            return {"error": "Gemini API Key non configurata"}

        prompt = f"""
        Agisci da analista betting professionista. Ti fornirò una lista di partite con:
        - Pronostico base di un esperto (Pengwin)
        - Quote di mercato (Eurobet)
        - Statistiche di classifica e forma (Sofascore)

        Dati:
        {json.dumps(matches_data, indent=2)}

        Obiettivo:
        Filtra il rumore e seleziona SOLO le 3-5 partite con il valore più alto (Value Bet).
        Scarta i match troppo incerti o con quote senza valore reale rispetto alle statistiche.

        Restituiscimi un file JSON rigoroso con questa struttura:
        [
          {{
            "Partita": "Nome Squadra A vs Nome Squadra B",
            "Campionato": "Serie A/Premier...",
            "Quota_Eurobet": "Valore quota",
            "Consiglio_Pengwin": "Il suo pronostico",
            "Giocata_Suggerita": "La tua giocata d'élite",
            "Analisi_Tecnica": "2-3 righe di motivazione basata sui dati"
          }},
          ...
        ]
        """

        try:
            response = self.model.generate_content(prompt)
            # Find JSON in response (Gemini sometimes adds markdown blocks)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text.strip())
        except Exception as e:
            return {"error": f"Errore durante l'analisi AI: {str(e)}"}

if __name__ == "__main__":
    # Test
    analyst = AIAnalyst()
    # print(analyst.analyze_matches([]))

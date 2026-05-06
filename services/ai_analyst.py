import google.generativeai as genai
import os
import json
import typing
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

        class MatchAnalysis(typing.TypedDict):
            Campionato: str
            Squadra_Casa: str
            Squadra_Trasferta: str
            Quota_Eurobet: str
            Consiglio_Pengwin: str
            Giocata_Suggerita: str
            Analisi_Tecnica: str
            Affidabilita_1_10: str

        prompt = f"""
        Agisci da analista betting professionista e amante del rischio leggero. Ti fornirò una lista di partite con quote e statistiche.
        Dati:
        {json.dumps(matches_data, indent=2)}

        Obiettivo:
        Seleziona SOLO le 3-5 partite con il valore più alto (Value Bet). 
        DEVI PRENDERE DEI RISCHI CALCOLATI: non limitarti alle quote basse e sicure. Cerca l'azzardo intelligente analizzando lo stato di forma (W/D/L, Posizione) e i consigli di Pengwin. Se vedi una squadra sfavorita (quota alta > 2.00) che però ha un'ottima forma recente rispetto all'avversario, SCEGLILA.
        Per ogni partita scelta, fornisci un'analisi dettagliata e aggressiva.
        """

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=list[MatchAnalysis]
                )
            )
            text = response.text
            
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

import asyncio
from scrapers.mondopengwin import MondopengwinScraper
from scrapers.eurobet import EurobetScraper
from services.sport_api import SportAPI
from services.ai_analyst import AIAnalyst
from services.reporter import Reporter

async def main():
    print("🚀 Avvio Analista Sportivo Virtuale...")
    
    # 1 & 2. Raccolta Dati Parallela (Pengwin + Eurobet)
    print("🔄 Avvio scrapers in parallelo...")
    pengwin = MondopengwinScraper()
    eurobet = EurobetScraper()
    
    predictions, odds = await asyncio.gather(
        pengwin.get_predictions(),
        eurobet.get_odds()
    )
    
    # 3. Integrazione Statistiche e Match Dati
    api = SportAPI()
    combined_data = []
    
    print("📊 Integrando statistiche Sofascore...")
    for pred in predictions:
        # Trova quote corrispondenti
        match_odds = next((o for o in odds if pred['teams'].lower() in o['teams'].lower() or o['teams'].lower() in pred['teams'].lower()), None)
        
        # Filtro Calendario: se non ci sono quote, la partita è passata o non disponibile
        if not match_odds:
            print(f"⏩ Salto {pred['teams']}: match già giocato o quote non disponibili.")
            continue
        
        # Recupera stats per entrambe le squadre
        if " vs " in pred['teams'] or "-" in pred['teams']:
            separator = " vs " if " vs " in pred['teams'] else "-"
            parts = pred['teams'].split(separator)
            team_home = parts[0].strip()
            team_away = parts[1].strip() if len(parts) > 1 else ""
        else:
            team_home = pred['teams'].split(" ")[0]
            team_away = ""

        stats = api.get_match_performance(team_home, team_away, pred['league']) if team_away else "Dati insuff."
        
        combined_data.append({
            "Match": pred['teams'],
            "Campionato": pred['league'],
            "Pronostico_Pengwin": pred['prediction'],
            "Quote_Eurobet": f"1:{match_odds['odds_1']} X:{match_odds['odds_x']} 2:{match_odds['odds_2']}" if match_odds else "N/D",
            "Statistiche_Sofascore": stats
        })

    # 4. Analisi AI
    print("🧠 Consultando l'analista AI...")
    analyst = AIAnalyst()
    top_picks = analyst.analyze_matches(combined_data)
    
    if isinstance(top_picks, dict) and "error" in top_picks:
        print(f"❌ Errore AI: {top_picks['error']}")
        return

    # 5. Generazione Report e Invio Telegram
    print("📄 Generando report Excel...")
    reporter = Reporter()
    excel_file = reporter.generate_excel(top_picks)
    
    if excel_file:
        reporter.send_to_telegram(excel_file)
        print("✅ Workflow completato con successo!")

if __name__ == "__main__":
    asyncio.run(main())

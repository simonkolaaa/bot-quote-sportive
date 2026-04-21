import asyncio
import logging
from scrapers.mondopengwin import MondopengwinScraper
from scrapers.eurobet import EurobetScraper
from services.sport_api import SportAPI
from services.ai_analyst import AIAnalyst
from services.reporter import Reporter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    logging.info("🚀 Avvio Analista Sportivo Virtuale...")
    
    # 1. Raccolta Pronostici Pengwin e Quote Eurobet (Concorrente)
    pengwin = MondopengwinScraper()
    eurobet = EurobetScraper()

    logging.info("Iniziando scraping in parallelo...")
    predictions, odds = await asyncio.gather(
        pengwin.get_predictions(),
        eurobet.get_odds()
    )
    
    # 3. Integrazione Statistiche e Match Dati
    api = SportAPI()
    combined_data = []
    
    logging.info("📊 Integrando statistiche Sofascore...")
    for pred in predictions:
        # Trova quote corrispondenti
        match_odds = next((o for o in odds if pred['teams'].lower() in o['teams'].lower() or o['teams'].lower() in pred['teams'].lower()), None)
        
        # Recupera stats per la squadra in casa (semplificato)
        team_home = pred['teams'].split(" vs ")[0] if " vs " in pred['teams'] else pred['teams'].split(" ")[0]
        stats = api.get_team_performance(team_home, pred['league'])
        
        combined_data.append({
            "Match": pred['teams'],
            "Campionato": pred['league'],
            "Pronostico_Pengwin": pred['prediction'],
            "Quote_Eurobet": f"1:{match_odds['odds_1']} X:{match_odds['odds_x']} 2:{match_odds['odds_2']}" if match_odds else "N/D",
            "Statistiche_Sofascore": stats
        })

    # 4. Analisi AI
    logging.info("🧠 Consultando l'analista AI...")
    analyst = AIAnalyst()
    top_picks = analyst.analyze_matches(combined_data)
    
    if isinstance(top_picks, dict) and "error" in top_picks:
        logging.error(f"❌ Errore AI: {top_picks['error']}")
        return

    # 5. Generazione Report e Invio Telegram
    logging.info("📄 Generando e inviando report Telegram...")
    reporter = Reporter()
    # Temporarily comment out excel while we refactor it in a later step
    # excel_file = reporter.generate_excel(top_picks)
    # if excel_file:
    #     reporter.send_to_telegram(excel_file)
    success = reporter.send_to_telegram(top_picks)
    
    if success:
        logging.info("✅ Workflow completato con successo!")
    else:
        logging.error("❌ Errore nell'invio del workflow!")

if __name__ == "__main__":
    asyncio.run(main())

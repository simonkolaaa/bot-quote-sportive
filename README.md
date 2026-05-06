# Bot Quote Sportive (AI Betting Analyst) 🤖📈

Un bot completamente automatizzato e containerizzato che raccoglie quote e pronostici, analizza le statistiche tramite AI (Gemini) e invia un report settimanale su Telegram con le migliori "Value Bets".

## 🚀 Caratteristiche Principali

- **Raccolta Dati Parallela**: Usa Playwright per scrapare i pronostici da MondoPengwin e le quote 1X2 da Eurobet in tempo reale.
- **Filtro Calendario Automatico**: Ignora automaticamente le partite già giocate o senza quote disponibili.
- **Statistiche in Tempo Reale**: Si collega a Sofascore tramite RapidAPI per recuperare la posizione in classifica e lo stato di forma (W/D/L) di entrambe le squadre in campo.
- **AI Analyst Spregiudicato**: Sfrutta Google Gemini (`gemini-2.5-flash`) con output strutturati (JSON). L'AI è istruita per assumersi "rischi calcolati", prediligendo le Value Bet con quote > 2.00 basandosi sulla forma reale delle squadre.
- **Notifiche Telegram**: Genera un file Excel formattato e lo invia direttamente sul tuo canale Telegram.
- **Dockerizzato & Schedulato**: Gira all'interno di un container isolato. Lo scheduler python fa partire il flusso ogni **Venerdì alle 10:00**.

## 🛠️ Prerequisiti

1. **Docker** e **Docker Compose** installati.
2. Un file `.env` nella root del progetto con le seguenti chiavi:
   ```env
   TELEGRAM_TOKEN=il_tuo_token_telegram
   CHAT_ID=il_tuo_chat_id
   X_RAPIDAPI_KEY=la_tua_key_rapidapi
   GEMINI_API_KEY=la_tua_key_gemini
   ```

## 🐳 Installazione e Avvio (Docker)

1. Crea e avvia il container in background:
   ```bash
   docker-compose up -d
   ```
2. Controlla i log per assicurarti che lo scheduler sia in attesa:
   ```bash
   docker-compose logs -f
   ```
   *Vedrai il messaggio: "🕒 Scheduler avviato. Il bot resterà in attesa e si attiverà ogni venerdì alle 10:00."*

## 🧪 Esecuzione Manuale

Se vuoi testare l'algoritmo ignorando lo scheduler (ad esempio per vedere subito quali partite consiglia l'AI):
```bash
# Esegui lo script direttamente dentro al container
docker-compose exec bot python main.py
```

## 🏗️ Struttura del Progetto
- `main.py`: L'orchestratore principale del flusso.
- `scheduler.py`: Il demone che tiene in vita il container e lancia `main.py` di venerdì.
- `scrapers/`: Contiene la logica per leggere i siti web (MondoPengwin, Eurobet).
- `services/`: Contiene le integrazioni API (`sport_api.py`), l'analisi AI (`ai_analyst.py`) e l'invio via Telegram (`reporter.py`).
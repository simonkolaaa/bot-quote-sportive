import schedule
import time
import asyncio
from datetime import datetime
from main import main

def run_job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Avvio del job schedulato (Venerdì ore 10:00)...")
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Errore critico durante l'esecuzione: {e}")

# Schedula l'esecuzione ogni venerdì alle 10:00
schedule.every().friday.at("10:00").do(run_job)

if __name__ == "__main__":
    print(f"🕒 Scheduler avviato ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}).")
    print("Il bot resterà in attesa e si attiverà ogni venerdì alle 10:00.")
    print("Per eseguire un test manuale immediato, lancia: python main.py")
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Controlla ogni minuto

import asyncio
from playwright.async_api import async_playwright

async def test_eurobet():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        url = "https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a"
        print(f"Navigazione a {url}...")
        await page.goto(url)
        
        try:
            await page.wait_for_selector(".bet-hub__row", timeout=30000)
            print("Righe trovate!")
        except:
            print("Timeout: nessuna riga .bet-hub__row trovata.")
            await browser.close()
            return

        rows = await page.query_selector_all(".bet-hub__row")
        print(f"Numero righe totali: {len(rows)}")
        
        for i, row in enumerate(rows[:5]):
            teams_el = await row.query_selector(".bet-hub__players")
            if teams_el:
                teams_text = await teams_el.inner_text()
                print(f"Row {i}: Squadre: {teams_text.replace('\n', ' ')}")
                odds = await row.query_selector_all(".odds__footer")
                print(f"Row {i}: Numero quote (.odds__footer): {len(odds)}")
                for j, odd in enumerate(odds):
                    val = await odd.inner_text()
                    print(f"  Quota {j}: {val.strip()}")
            else:
                print(f"Row {i}: Nessun .bet-hub__players trovato")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_eurobet())

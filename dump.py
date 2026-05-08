import asyncio
from playwright.async_api import async_playwright

async def dump_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Dump Eurobet
        print("Dumping Eurobet...")
        await page.goto("https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a")
        await asyncio.sleep(5)
        with open("eurobet_live.html", "w", encoding="utf-8") as f:
            f.write(await page.content())
            
        # Dump Pengwin
        print("Dumping Pengwin...")
        await page.goto("https://www.mondopengwin.it/pronostici/calcio/serie-a/")
        await asyncio.sleep(5)
        with open("pengwin_live.html", "w", encoding="utf-8") as f:
            f.write(await page.content())

        # Grab a specific article from Pengwin
        articles = await page.query_selector_all("a")
        article_url = None
        for art in articles:
            href = await art.get_attribute("href")
            if href and "statistiche-quote-e-pronostico" in href.lower():
                article_url = href
                break
                
        if article_url:
            print(f"Dumping Pengwin Article: {article_url}...")
            await page.goto(article_url)
            await asyncio.sleep(3)
            with open("pengwin_article_live.html", "w", encoding="utf-8") as f:
                f.write(await page.content())
                
        await browser.close()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(dump_pages())

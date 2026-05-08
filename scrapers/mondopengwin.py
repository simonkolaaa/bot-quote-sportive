import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import re

class MondopengwinScraper:
    def __init__(self):
        self.base_url = "https://www.mondopengwin.it/pronostici/calcio/"
        self.leagues = ["serie-a", "premier-league", "la-liga"]

    async def get_predictions(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
            await Stealth().apply_stealth_async(page)
            
            all_predictions = []

            for league in self.leagues:
                url = f"{self.base_url}{league}/"
                print(f"Scraping league: {league}...")
                await page.goto(url)
                
                # Handle cookie/disclaimer if present
                try:
                    # Accept cookies - coordinate generic check
                    await asyncio.sleep(2)
                    
                    # Cerca pulsante PROMETTO
                    prometto_btn = await page.wait_for_selector('button:has-text("PROMETTO")', timeout=10000)
                    if prometto_btn:
                        await prometto_btn.click()
                        print("  Pop-up 'PROMETTO' chiuso.")
                except:
                    pass

                # Get all article links
                articles = await page.query_selector_all("a")
                article_urls = []
                for art in articles:
                    href = await art.get_attribute("href")
                    if href and "statistiche-quote-e-pronostico" in href.lower() and href not in article_urls:
                        article_urls.append(href)

                for art_url in article_urls[:5]: # Limit to last 5 articles
                    await page.goto(art_url)
                    await asyncio.sleep(1)
                    
                    try:
                        title_el = await page.query_selector("h1.title")
                        if not title_el:
                            title_el = await page.query_selector("h1")
                        
                        title = await title_el.inner_text()
                        teams = title.split(" STATISTICHE")[0].split(" ANALISI")[0].replace("-", " ").strip()
                        
                        # Extract prediction from #pengwincontent
                        content_el = await page.query_selector("#pengwincontent")
                        if not content_el:
                            content_el = await page.query_selector(".entry-content")
                            
                        content = await content_el.inner_text()
                        
                        prediction = "Non trovato"
                        search_str = "Analisi e pronostico di Kristian Pengwin:"
                        if search_str in content:
                            sub_content = content.split(search_str)[-1]
                            if "Non ancora disponibile" in sub_content:
                                prediction = "Non ancora disponibile."
                            else:
                                # Look for sentences containing keywords
                                sentences = sub_content.replace('\n', ' ').split('.')
                                for s in sentences:
                                    if 'pronostico' in s.lower() or 'quota' in s.lower() or 'combo' in s.lower() or 'puntare' in s.lower():
                                        prediction = s.strip() + "."
                                        break
                        
                        all_predictions.append({
                            "league": league,
                            "teams": teams,
                            "prediction": prediction,
                            "url": art_url
                        })
                        print(f"  Found: {teams} -> {prediction}")
                    except Exception as e:
                        print(f"  Error parsing article {art_url}: {e}")
                        continue

            await browser.close()
            return all_predictions

if __name__ == "__main__":
    scraper = MondopengwinScraper()
    results = asyncio.run(scraper.get_predictions())
    print(f"Total predictions found: {len(results)}")

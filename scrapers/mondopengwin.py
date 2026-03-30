import asyncio
from playwright.async_api import async_playwright
import re

class MondopengwinScraper:
    def __init__(self):
        self.base_url = "https://www.mondopengwin.it/pronostici/calcio/"
        self.leagues = ["serie-a", "premier-league", "la-liga"]

    async def get_predictions(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            all_predictions = []

            for league in self.leagues:
                url = f"{self.base_url}{league}/"
                print(f"Scraping league: {league}...")
                await page.goto(url)
                
                # Handle cookie/disclaimer if present
                try:
                    # Accept cookies
                    cookie_btn = await page.wait_for_selector('button:has-text("Accetto")', timeout=5000)
                    if cookie_btn:
                        await cookie_btn.click()
                    
                    # Handle "PROMETTO" if it pops up
                    prometto_btn = await page.wait_for_selector('button:has-text("PROMETTO")', timeout=5000)
                    if prometto_btn:
                        await prometto_btn.click()
                except:
                    pass

                # Get all article links
                articles = await page.query_selector_all(".article_title a")
                article_urls = [await art.get_attribute("href") for art in articles]

                for art_url in article_urls[:10]: # Limit to last 10 articles for now
                    if "pronostico" not in art_url.lower():
                        continue
                        
                    await page.goto(art_url)
                    
                    title = await page.inner_text("h1")
                    # Extract teams from title (usually TEAM-A-TEAM-B-...)
                    teams = title.split(" STATISTICHE")[0].replace("-", " ")
                    
                    # Extract prediction
                    content = await page.inner_text(".entry-content")
                    
                    # Look for the "proposta base" section
                    prediction = "Non trovato"
                    search_str = "Analisi e pronostico di Kristian Pengwin:"
                    if search_str in content:
                        parts = content.split(search_str)
                        if len(parts) > 1:
                            # The prediction is usually in the last few paragraphs of this section
                            sub_content = parts[1]
                            # Look for "proposta base" or similar
                            match = re.search(r"(?:proposta base|giocata consigliata|Il nostro consiglio|pronostico).*?:?\s*(.*)", sub_content, re.IGNORECASE)
                            if match:
                                prediction = match.group(1).strip().split("\n")[0]
                    
                    all_predictions.append({
                        "league": league,
                        "teams": teams,
                        "prediction": prediction,
                        "url": art_url
                    })
                    print(f"  Found: {teams} -> {prediction}")

            await browser.close()
            return all_predictions

if __name__ == "__main__":
    scraper = MondopengwinScraper()
    results = asyncio.run(scraper.get_predictions())
    print(f"Total predictions found: {len(results)}")

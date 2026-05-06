import asyncio
from playwright.async_api import async_playwright

class EurobetScraper:
    def __init__(self):
        self.leagues = {
            "serie-a": "https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a",
            "premier-league": "https://www.eurobet.it/it/scommesse/#!/calcio/en-premier-league",
            "la-liga": "https://www.eurobet.it/it/scommesse/#!/calcio/es-la-liga"
        }

    async def get_odds(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            all_odds = []

            for league_name, url in self.leagues.items():
                print(f"Scraping odds for: {league_name}...")
                await page.goto(url)
                
                # Handle cookie banner
                try:
                    cookie_btn = await page.wait_for_selector('button:has-text("Accetto")', timeout=10000)
                    if cookie_btn:
                        await cookie_btn.click()
                except:
                    pass

                # Wait for match cards to load
                try:
                    await page.wait_for_selector(".bet-hub__row", timeout=30000)
                except:
                    print(f"  Timeout waiting for matches in {league_name}")
                    continue

                # Get all match containers
                match_elements = await page.query_selector_all(".bet-hub__row")
                
                for element in match_elements:
                    try:
                        # Extract team names
                        teams_el = await element.query_selector(".bet-hub__players")
                        if not teams_el:
                            continue
                        teams_text = await teams_el.inner_text()
                        teams = teams_text.replace("\n", " - ")
                        
                        # Extract odds (1, X, 2)
                        # The pattern for 1X2 market is usually the first 3 odds buttons
                        odds_labels = await element.query_selector_all(".odds__footer")
                        if len(odds_labels) >= 3:
                            odd_1 = await odds_labels[0].inner_text()
                            odd_x = await odds_labels[1].inner_text()
                            odd_2 = await odds_labels[2].inner_text()
                            
                            all_odds.append({
                                "league": league_name,
                                "teams": teams,
                                "odds_1": odd_1.strip(),
                                "odds_x": odd_x.strip(),
                                "odds_2": odd_2.strip()
                            })
                            print(f"  Match: {teams} | 1: {odd_1}, X: {odd_x}, 2: {odd_2}")
                    except Exception as e:
                        # print(f"  Error parsing match: {e}")
                        continue

            await browser.close()
            return all_odds

if __name__ == "__main__":
    scraper = EurobetScraper()
    results = asyncio.run(scraper.get_odds())
    print(f"Total matches found: {len(results)}")

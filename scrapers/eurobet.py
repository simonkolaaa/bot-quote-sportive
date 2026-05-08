import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

class EurobetScraper:
    def __init__(self):
        self.leagues = {
            "serie-a": "https://www.eurobet.it/it/scommesse/#!/calcio/it-serie-a",
            "premier-league": "https://www.eurobet.it/it/scommesse/#!/calcio/en-premier-league",
            "la-liga": "https://www.eurobet.it/it/scommesse/#!/calcio/es-la-liga"
        }

    async def get_odds(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
            await Stealth().apply_stealth_async(page)
            
            all_odds = []

            for league_name, url in self.leagues.items():
                print(f"Scraping odds for: {league_name}...")
                await page.goto(url)
                
                # Handle cookie banner
                try:
                    cookie_btn = await page.wait_for_selector('button#onetrust-accept-btn-handler', timeout=5000)
                    if cookie_btn:
                        await cookie_btn.click()
                except:
                    pass
                
                # Attesa del caricamento dinamico
                await asyncio.sleep(5)

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
                        teams_el = await element.query_selector_all(".bet-hub__players div")
                        if len(teams_el) < 2:
                            continue
                        team_home = await teams_el[0].inner_text()
                        team_away = await teams_el[1].inner_text()
                        teams = f"{team_home.strip()} - {team_away.strip()}"
                        
                        # Extract odds (1, X, 2)
                        odd_1_el = await element.query_selector("div:nth-child(4) div")
                        odd_x_el = await element.query_selector("div:nth-child(5) div")
                        odd_2_el = await element.query_selector("div:nth-child(6) div")
                        
                        if odd_1_el and odd_x_el and odd_2_el:
                            odd_1 = await odd_1_el.inner_text()
                            odd_x = await odd_x_el.inner_text()
                            odd_2 = await odd_2_el.inner_text()
                            
                            all_odds.append({
                                "league": league_name,
                                "teams": teams,
                                "odds_1": odd_1.replace('\n', ' ').strip(),
                                "odds_x": odd_x.replace('\n', ' ').strip(),
                                "odds_2": odd_2.replace('\n', ' ').strip()
                            })
                            print(f"  Match: {teams} | 1: {odd_1}, X: {odd_x}, 2: {odd_2}")
                    except Exception as e:
                        print(f"  Error parsing match: {e}")
                        continue

            await browser.close()
            return all_odds

if __name__ == "__main__":
    scraper = EurobetScraper()
    results = asyncio.run(scraper.get_odds())
    print(f"Total matches found: {len(results)}")

import asyncio
from scrapers.eurobet import EurobetScraper

async def test_eurobet():
    scraper = EurobetScraper()
    results = await scraper.get_odds()
    print(f"Quote trovate: {len(results)}")
    for r in results:
        print(f"  {r['teams']} ({r['league']}) -> 1:{r['odds_1']} X:{r['odds_x']} 2:{r['odds_2']}")

if __name__ == "__main__":
    asyncio.run(test_eurobet())

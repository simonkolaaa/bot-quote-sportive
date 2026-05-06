import asyncio
from scrapers.mondopengwin import MondopengwinScraper

async def test_pengwin():
    scraper = MondopengwinScraper()
    results = await scraper.get_predictions()
    print(f"Predizioni trovate: {len(results)}")
    for r in results:
        print(f"  {r['teams']} ({r['league']}) -> {r['prediction']}")

if __name__ == "__main__":
    asyncio.run(test_pengwin())

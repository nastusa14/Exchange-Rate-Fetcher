import aiohttp
import asyncio
import datetime
from typing import List, Dict, Any

# Constants
BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
CURRENCIES = ["USD", "EUR"]
MAX_DAYS = 10

class ExchangeRateFetcher:
    def __init__(self):
        self.base_url = BASE_URL

    async def fetch_rate(self, session: aiohttp.ClientSession, date: str) -> Dict[str, Any]:
        url = f"{self.base_url}{date}"
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Error fetching data for date {date}: {response.status}")
            data = await response.json()
            rates = {currency: self._extract_rate(data, currency) for currency in CURRENCIES}
            return {date: rates}

    @staticmethod
    def _extract_rate(data: dict, currency: str) -> Dict[str, float]:
        for rate in data.get("exchangeRate", []):
            if rate.get("currency") == currency:
                return {
                    "sale": rate.get("saleRate", 0.0),
                    "purchase": rate.get("purchaseRate", 0.0)
                }
        return {"sale": 0.0, "purchase": 0.0}

class ExchangeRateService:
    def __init__(self, fetcher: ExchangeRateFetcher):
        self.fetcher = fetcher

    async def get_rates(self, days: int) -> List[Dict[str, Any]]:
        if days > MAX_DAYS:
            raise ValueError(f"Days cannot be more than {MAX_DAYS}")

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i in range(days):
                date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d.%m.%Y")
                tasks.append(self.fetcher.fetch_rate(session, date))
            results = await asyncio.gather(*tasks)
        
        return results

class ExchangeRateCLI:
    def __init__(self, service: ExchangeRateService):
        self.service = service

    async def run(self, days: int):
        try:
            rates = await self.service.get_rates(days)
            print(rates)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python exchange_rate.py <days>")
        sys.exit(1)

    days = int(sys.argv[1])

    fetcher = ExchangeRateFetcher()
    service = ExchangeRateService(fetcher)
    cli = ExchangeRateCLI(service)

    asyncio.run(cli.run(days))
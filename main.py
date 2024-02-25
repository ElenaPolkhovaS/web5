import argparse
import aiohttp
import asyncio
from datetime import datetime, timedelta

async def fetch_exchange_rates(session, date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    async with session.get(url) as response:
        data = await response.json()
        return data

async def get_currency_rates(days):
    async with aiohttp.ClientSession() as session:
        tasks = []
        current_date = datetime.now()

        for day in range(days):
            date = (current_date - timedelta(days=day)).strftime('%d.%m.%Y')
            tasks.append(fetch_exchange_rates(session, date))

        results = await asyncio.gather(*tasks)

        formatted_results = []
        for i, date in enumerate(results):
            formatted_result = f"{date['date']}:\n"
            for currency in date['exchangeRate']:
                if currency['currency'] in ['EUR', 'USD']:
                    formatted_result += f"  {currency['currency']}:\n"
                    formatted_result += f"    Sale: {currency['saleRateNB']}\n"
                    formatted_result += f"    Purchase: {currency['purchaseRateNB']}\n"
            formatted_results.append(formatted_result)

        return formatted_results

def parse_arguments():
    parser = argparse.ArgumentParser(description='Get currency exchange rates from PrivatBank')
    parser.add_argument('days', type=int, help='Number of days to retrieve exchange rates (max 10)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.days > 10:
        print("Error: Number of days should not exceed 10.")
        return

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_currency_rates(args.days))
    for entry in result:
        print(entry)

if __name__ == '__main__':
    main()

import platform
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


async def get_exchange_rates(days):
    async with aiohttp.ClientSession() as session:
        tasks = []
        current_date = datetime.now()

        for day in range(days):
            date = (current_date - timedelta(days=day)).strftime('%d.%m.%Y')
            tasks.append(fetch_exchange_rates(session, date))

        results = await asyncio.gather(*tasks)

        formatted_results = []
        for i, date in enumerate(results):
            formatted_result = {date['date']: {}}
            for currency in date['exchangeRate']:
                formatted_result[date['date']][currency['currency']] = {
                    'sale': currency['saleRateNB'],
                    'purchase': currency['purchaseRateNB']
                }
            formatted_results.append(formatted_result)

        return formatted_results


async def main():
    while True:
        command = input("Введіть команду ('exchange' для отримання курсу валют, 'exit' для виходу): ")

        if command == 'exit':
            break
        elif command.startswith('exchange'):
            try:
                _, days_str = command.split(' ')
                days = int(days_str)
                if days <= 10:
                    result = await get_currency_rates(days)
                    print("\nКурс валют:")
                    for entry in result:
                        print(entry)
                else:
                    print("Помилка: Кількість днів повинна бути не більше 10.")
            except ValueError:
                print("Помилка: Введіть коректну кількість днів.")
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
           
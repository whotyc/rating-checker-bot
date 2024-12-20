import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot

TELEGRAM_TOKEN = ''
CHAT_ID = ''

USERNAME = ''

URL = ''


async def get_rating():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Error on page retrieval")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        print("Table not found")
        return None

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1 and USERNAME in cells[1].text:
            rating = cells[0].text.strip()
            return rating

    print("Your rating was not found")
    return None


async def send_message(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    while True:
        rating = await get_rating()
        if rating:
            await send_message(bot, f"Your rating for {USERNAME}: {rating}")
        await asyncio.sleep(1800)


if __name__ == "__main__":
    asyncio.run(main())
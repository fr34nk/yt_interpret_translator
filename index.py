from gemini import GeminiAsker
import asyncio
import aiohttp
from bot import Bot

if __name__ == '__main__':
    # asker = GeminiAsker()
    # asyncio.run(asker.main())

    bot = Bot("prompter")
    bot.exec()






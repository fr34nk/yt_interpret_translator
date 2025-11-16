#!/usr/bin/env python3
import asyncio
import aiohttp
import json
import os
from typing import Optional, Union

API_KEY = os.getenv("GEMINI_API_KEY")

# ----- Conversation Memory -----

class GeminiAsker:
    queue: asyncio.Queue = asyncio.Queue()

    BASE_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"


    conversation = [
        {"parts": [{"text": "You are a helpful assistant."}]}
    ]

    def __init__ (self):
        self.queue = asyncio.Queue()
        return None

    async def gemini_worker (self):
        """Worker that processes user messages from the queue."""
        async with aiohttp.ClientSession() as session:
            while True:
                user_message = await self.queue.get()

                # Add user message to history
                self.conversation.append({"parts": [{"text": user_message}]})

                payload = {"contents": self.conversation}

                async with session.post(
                    self.BASE_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload)
                ) as resp:
                    data = await resp.json()

                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                self.conversation.append({"parts": [{"text": reply}]})

                print(f"\nGemini: {reply}\nYou: ", end="", flush=True)

                self.queue.task_done()

    async def input_loop (self):
        """Reads user input without blocking the worker."""
        while True:
            user_message = await asyncio.to_thread(input, "You: ")
            await self.queue.put(user_message)


    async def main (self):
        worker = asyncio.create_task(self.gemini_worker())
        inputter = asyncio.create_task(self.input_loop())

        await asyncio.gather(worker, inputter)


if __name__ == "__main__":
    asker = GeminiAsker()
    asyncio.run(asker.main())



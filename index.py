import asyncio
import aiohttp
import json
import os

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = (
    f"https://generativelanguage.googleapis.com/v1/models/"
    f"gemini-2.5-flash:generateContent?key={API_KEY}"
)

# ----- Conversation Memory -----
conversation = [
    {"parts": [{"text": "You are a helpful assistant."}]}
]

# ----- Message Queue -----
queue = asyncio.Queue()


async def gemini_worker():
    """Worker that processes user messages from the queue."""
    async with aiohttp.ClientSession() as session:
        while True:
            user_message = await queue.get()

            # Add user message to history
            conversation.append({"parts": [{"text": user_message}]})

            payload = {"contents": conversation}

            async with session.post(
                BASE_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            ) as resp:
                data = await resp.json()

            # Extract model reply
            reply = data["candidates"][0]["content"]["parts"][0]["text"]

            # Add assistant message to history
            conversation.append({"parts": [{"text": reply}]})

            print(f"\nGemini: {reply}\nYou: ", end="", flush=True)

            queue.task_done()


async def input_loop():
    """Reads user input without blocking the worker."""
    while True:
        user_message = await asyncio.to_thread(input, "You: ")
        await queue.put(user_message)


async def main():
    worker = asyncio.create_task(gemini_worker())
    inputter = asyncio.create_task(input_loop())

    await asyncio.gather(worker, inputter)


if __name__ == "__main__":
    asyncio.run(main())


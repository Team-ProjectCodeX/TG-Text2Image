# CREATED BY: https://t.me/O_oKarma
# API CREDITS: @Qewertyy
# PROVIDED BY: https://github.com/Team-ProjectCodeX


import asyncio

from httpx import AsyncClient as AsyncHttpxClient
from pyrogram import filters

from Repo import app

BASE_URL = "https://lexica.qewertyy.me"
SESSION_HEADERS = {"Host": "lexica.qewertyy.me"}


class AsyncClient:
    def __init__(self):
        self.url = BASE_URL
        self.session = AsyncHttpxClient(
            http2=True,
            headers=SESSION_HEADERS,
        )

    async def generate(self, model_id, prompt, negative_prompt):
        data = {
            "model_id": model_id,
            "prompt": prompt,
            "negative_prompt": negative_prompt if negative_prompt else "",
            "num_images": 1,
        }
        try:
            resp = await self.session.post(f"{self.url}/models/inference", data=data)
            return resp.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")

    async def get_images(self, task_id, request_id):
        data = {"task_id": task_id, "request_id": request_id}
        try:
            resp = await self.session.post(
                f"{self.url}/models/inference/task", data=data
            )
            return resp.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")


async def generate_image_handler(client, message, model_id):
    command_parts = message.text.split(" ", 1)
    if len(command_parts) < 2:
        await message.reply("Please provide a prompt.")
        return

    prompt = command_parts[1]
    negative_prompt = ""

    # Send the initial "Generating your image, wait sometime" message
    reply_message = await message.reply("Generating your image, please wait...")

    client = AsyncClient()
    response = await client.generate(model_id, prompt, negative_prompt)
    task_id = response["task_id"]
    request_id = response["request_id"]

    while True:
        generated_images = await client.get_images(task_id, request_id)

        if "img_urls" in generated_images:
            for img_url in generated_images["img_urls"]:
                # Delete the initial reply message
                await reply_message.delete()

                # Send the generated image
                await message.reply_photo(img_url)
            break  # Exit the loop when images are available
        else:
            # Wait for a few seconds before checking again
            await asyncio.sleep(5)

        # Optionally, you can add a timeout to avoid an infinite loop
        timeout_seconds = 200  # 10 minutes (adjust as needed)
        if timeout_seconds <= 0:
            await reply_message.edit("Image generation timed out.")
            break

        timeout_seconds -= 5  # Decrement timeout by 5 seconds


@app.on_message(filters.command("meinamix", prefixes="/"))
async def meinamix_handler(client, message):
    await generate_image_handler(client, message, model_id=2)


@app.on_message(filters.command("darksushi", prefixes="/"))
async def darksushi_handler(client, message):
    await generate_image_handler(client, message, model_id=7)


@app.on_message(filters.command("meinahentai", prefixes="/"))
async def meinahentai_handler(client, message):
    await generate_image_handler(client, message, model_id=8)


@app.on_message(filters.command("darksushimix", prefixes="/"))
async def darksushimix_handler(client, message):
    await generate_image_handler(client, message, model_id=9)


@app.on_message(filters.command("anylora", prefixes="/"))
async def anylora_handler(client, message):
    await generate_image_handler(client, message, model_id=3)


@app.on_message(filters.command("anything", prefixes="/"))
async def anything_handler(client, message):
    await generate_image_handler(client, message, model_id=4)


@app.on_message(filters.command("cetusmix", prefixes="/"))
async def cetusmix_handler(client, message):
    await generate_image_handler(client, message, model_id=10)


@app.on_message(filters.command("absolute", prefixes="/"))
async def absolute_handler(client, message):
    await generate_image_handler(client, message, model_id=13)


@app.on_message(filters.command("darkv2", prefixes="/"))
async def darkv_handler(client, message):
    await generate_image_handler(client, message, model_id=14)


@app.on_message(filters.command("creative", prefixes="/"))
async def creative_handler(client, message):
    await generate_image_handler(client, message, model_id=12)

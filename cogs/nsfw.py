import disnake
from disnake.ext import commands
import random
import aiohttp
import json

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="Поиск картинок на rule34.xxx", 
    )
    @commands.is_nsfw()
    async def rule34(
        self,
        inter,
        count: commands.Range(int, 0, 30) = commands.Param(1, description="Количество картинок для вывода"),
        tags: str = commands.Param(
            name="поиск",
            description="Укажите тег для поиска, например: boy",
        )
    ):
        await inter.response.defer()

        results = []

        tags_message = f"Теги: {tags}\n"
        for _ in range(count):
            if id is None:
                async with aiohttp.request(
                    "GET",
                    f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&tags={tags}&json=1",
                ) as resp:
                    data = await resp.json()
            else:
                async with aiohttp.request(
                    "GET",
                    f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&id={id}&json=1",
                ) as resp:
                    data = await resp.json()

            if data is None:
                return await inter.send(
                    embed=disnake.Embed(
                        description="Результаты не найдены.",
                        color=0x2b2d31,
                    ),
                )

            keyses = len(data) - 1
            rand = random.randint(0, keyses)
            result = {"url": data[rand]["file_url"]}
            results.append(result)

        messages = [tags_message]
        for i, result in enumerate(results, start=1):
            messages.append(f"[{i}] {result['url']}")

        await inter.send(content="\n".join(messages))

def setup(bot):
    bot.add_cog(NSFW(bot))

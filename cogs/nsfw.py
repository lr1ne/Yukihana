import disnake
from disnake.ext import commands, components
import random
import aiohttp
import json

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        description="😀 Развлечения | Выводит рандомную картинку для взрослых (поиск на rule34)"
    )
    async def nsfw(
        self,
        inter,
        count: commands.Range[int, 0, 30] = commands.Param(1, description="Количество картинок для вывода"),
        tags: str = commands.Param(
            name="поиск",
            description="Укажите тег для поиска, например: boy",
        ),
        id: int = commands.Param(
            None,
            description="Укажите ID публикации (при неверном ID будет показана рандомная картинка)",
        ),
    ):
        if inter.channel.is_nsfw():
            await inter.response.defer()

            results = []

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
                    return await inter.edit_original_message(
                        embed=disnake.Embed(
                            description="Результаты не найдены, попробуйте поискать с помощью таких тегов как:\n `cum penis anal gay` через пробел",
                            color=0x2b2d31,
                        ),
                    )

                keyses = len(data) - 1
                rand = random.randint(0, keyses)
                result = {"url": data[rand]["file_url"]}
                results.append(result)

            chunk_size = 10
            for i in range(0, len(results), chunk_size):
                chunk = results[i:i+chunk_size]
                messages = []
                for result in chunk:
                    messages.append(f"Теги: {tags} \n{result['url']}")
                await inter.send(content="\n".join(messages))

        else:
            embed = disnake.Embed(
                description="Никакого NSFW в данном канале - только чистый и здоровый контент!",
                color=0x2b2d31,
            )
            await inter.edit_original_message(embed=embed)

def setup(bot):
    bot.add_cog(NSFW(bot))

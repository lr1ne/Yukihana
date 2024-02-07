from disnake.ext import commands
from os import listdir
import disnake
import aiohttp
from config import settings

class Yukihana(commands.Bot):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {bot.user}')
        # # URL of the animated avatar
        # avatar_url = 'https://media1.tenor.com/m/PFeI000LYHkAAAAC/boy-kisser-boykisser.gif'
        # try:
        #     async with aiohttp.ClientSession() as session:
        #         async with session.get(avatar_url) as response:
        #             if response.status == 200:
        #                 avatar_data = await response.read()
        #                 await bot.user.edit(avatar=avatar_data)
        #                 print('Animated avatar uploaded successfully!')
        #             else:
        #                 print('Failed to download avatar:', response.status)
        # except Exception as e:
        #     print('Failed to upload animated avatar:', e)
        
bot = Yukihana(
    command_prefix=settings['prefix'],
    intents=disnake.Intents.all(),
    owner_ids=settings['owner_id']
)

list_cogs = [filename[:-3] for filename in listdir("./cogs") if filename.endswith(".py")]
for cog in list_cogs: bot.load_extension(f"cogs.{cog}")
bot.load_extension('jishaku')

@bot.slash_command(description=f'Загрузить модуль бота')
@commands.is_owner()
async def load(inter, module: str = commands.Param(description="Название модуля")):
    bot.load_extension(f"cogs.{module}")
    await inter.send(f"Загружен модуль `{module}`", ephemeral=True)


@bot.slash_command(description=f'Выгрузить модуль бота')
@commands.is_owner()
async def unload(inter, module: str = commands.Param(description="Название модуля")):
    bot.unload_extension(f"cogs.{module}")
    await inter.send(f"Выгружен модуль `{module}`", ephemeral=True)


@bot.slash_command(description=f"Перезагрузить модуль бота")
@commands.is_owner()
async def reload(inter, module: str = commands.Param(description="Название модуля", choices=list_cogs)):
    bot.reload_extension(f"cogs.{module}")
    await inter.send(f"Перезагружен модуль `{module}`", ephemeral=True)

bot.run(settings['token'])

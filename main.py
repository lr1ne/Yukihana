from disnake.ext import commands
from os import listdir
import disnake
from config import settings

class Yukihana(commands.Bot):
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Запущен!")
        
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

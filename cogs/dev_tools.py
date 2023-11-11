### Ког, в котором я соберу все команды и ивенты, которые доступны ТОЛЬКО тем, чье ID есть в файле config.py

import disnake
from disnake.ext import commands
import datetime as DT
import time

start_time = time.time()

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="uptime", description="-- ONLY FOR DEVELOPER --")
    @commands.is_owner()
    async def uptime(self, inter):
        dt = DT.datetime.fromisoformat(f"{time.time() - start_time}")
        timestamp = int(dt.timestamp())
        embed = disnake.Embed(
            title="Аптайм бота.",
            description=""
        )
        embed.add_field(name="Bot Uptime", value=f"Бот был запущен <t:{timestamp}:R>"
                                                 f"Пинг - {(round(self.bot.latency * 1000))} ms")
        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(DevTools(bot))

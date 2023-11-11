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
        dt = DT.datetime.fromisoformat(time.time() - start_time)
        timestamp = int(dt.timestamp())
        embed = disnake.Embed(
            title="Аптайм бота.",
            description=""
        )
        embed.add_field(name="Bot Uptime", value=f"Бот был запущен <t:{timestamp}:R>"
                                                 f"Пинг - {(round(self.bot.latency * 1000))} ms")
        await inter.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, commands.Cooldown):
            return
        channel = self.bot.get_channel(1172161193612410972)
        timestamp = int(DT.timestamp(DT.now()))
        command = inter.permissions.value
        if command == 562949953421311:
            command = "562949953421311 - Все права"
        if command == 8:
            command = "8 - Администратор"
        name = inter.application_command.name
        embed = disnake.Embed(description=f"`💔` <t:{timestamp}:f> (<t:{timestamp}:R>) Последний вызов вызвал исключение:\n```cmd\n{error}\n```"
                                          f"\nКод разрешений: \n```\n{command}\n```\nСервер: {inter.guild.name}\nПользователь: {inter.author.name}\nID сервера: {inter.guild.id}\nID участника: {inter.author.id}"
                                          f"\n Команда: </{name}:{inter.data.id}>",
                              color=disnake.Colour.red())
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(DevTools(bot))

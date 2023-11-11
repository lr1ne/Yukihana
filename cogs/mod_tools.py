import disnake
import re
from disnake.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Команда для мута пользователя
    @commands.slash_command(name="mute", description="Замутить человека")
    async def mute(self, inter,
                   member: disnake.Member = commands.Param(name='пользователь', description="Пользователь для мута"),
                   duration: str = commands.Param(name="время", description="1w, 1d, 15h, 30m, 30s"),
                   reason: str = commands.Param("Не указана", name="причина", description="Причина мута")):
        durations = duration.split()

        # Проверки на наличие прав
        if member.id == inter.guild.owner_id:
            return await inter.send("Нельзя замутить владельца сервера", ephemeral=True)
        if member.current_timeout is not None:
            return await inter.send("Пользователь уже замучен", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Ваша роль ниже роли пользователя, которого Вы хотите заглушить!", ephemeral=True)
        if member.top_role >= inter.guild.me.top_role:
            return await inter.send("Моя роль ниже роли пользователя, которого Вы хотите заглушить!", ephemeral=True)
        
        # Проверка на правильность ввода времени
        for dur in durations:
            if not re.match(r'^\d+[wdhms]$', dur):
                raise commands.BadArgument("Неверный формат времени. Используйте формат 1d, 2h, 3m через запятую или пробел")

        # Перевод времени в секунды
        total_seconds = 0
        for dur in durations:
            val = int(dur[:-1])
            unit = dur[-1].lower()
            if unit == 's':
                total_seconds += val
            elif unit == 'm':
                total_seconds += val * 60
            elif unit == 'h':
                total_seconds += val * 60 * 60
            elif unit == 'd':
                total_seconds += val * 24 * 60 * 60
            elif unit == 'w':
                total_seconds += val * 7 * 24 * 60 * 60

        # Перевод времени в формат 1w 2d 3h 4m 5s
        weeks = total_seconds // (7 * 24 * 60 * 60)
        days = (total_seconds // (24 * 60 * 60)) % 7
        hours = (total_seconds // (60 * 60)) % 24
        minutes = (total_seconds // 60) % 60
        seconds = total_seconds % 60

        # Форматирование времени
        time_formatted = ""
        if weeks > 1:
            time_formatted += f"{weeks} недели"
        if weeks > 0:
            time_formatted += f"{weeks} неделя"
        if days > 5:
            time_formatted += f"{days} дней"
        if days > 1:
            time_formatted += f"{days} дня"
        if days > 0:
            time_formatted += f"{days} день"
        if hours > 5:
            time_formatted += f"{hours} часов"
        if hours > 1:
            time_formatted += f"{hours} часа"
        if hours > 0:
            time_formatted += f"{hours} час"
        if minutes > 5:
            time_formatted += f"{minutes} минут"
        if minutes > 1:
            time_formatted += f"{minutes} минуты"
        if minutes > 0:
            time_formatted += f"{minutes} минута"
        if seconds > 5:
            time_formatted += f"{seconds} секунд"
        if seconds > 1:
            time_formatted += f"{seconds} секунды"
        if seconds > 0:
            time_formatted += f"{seconds} секунд"

        # Отправка сообщения в канал
        embed = disnake.Embed(
            title="Мут",
            description="",
            color=0x2b2d31
        )
        embed.add_field(name="*Помолчи немного!*", value=f"Модератор {inter.author.mention} замутил пользователя {member.mention}.\n"
                                                            f"Причина: {reason}\n"
                                                            f"Молчание продлится {time_formatted}", inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon.url)
        await inter.send(embed=embed)
        await member.edit(timeout=total_seconds, reason=reason)

    # Обработка ошибок
    @mute.error
    async def mute_error(self, inter, error):
        if isinstance(error, commands.BotMissingPermissions):
            await inter.send("У меня недостаточно прав для выполнения этой команды!", ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            await inter.send("У вас недостаточно прав для выполнения этой команды!", ephemeral=True)

    # Команда для размута пользователя
    @commands.slash_command(name="unmute", description="Размутить человека")
    async def unmute(self, inter,
                     member: disnake.Member = commands.Param(name='пользователь', description="Пользователь для размута")):
        # Проверки на наличие прав
        if member.id == inter.guild.owner_id:
            return await inter.send("Нельзя размутить владельца сервера", ephemeral=True)
        if member.current_timeout is None:
            return await inter.send("Пользователь не замучен", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Ваша роль ниже роли пользователя, которого Вы хотите размутить!", ephemeral=True)
        if member.top_role >= inter.guild.me.top_role:
            return await inter.send("Моя роль ниже роли пользователя, которого Вы хотите размутить!", ephemeral=True)
        
        # Размут пользователя
        embed = disnake.Embed(
            title="Размут",
            description="",
            color=0x2b2d31
        )
        embed.add_field(name="*Ну ладно, можешь говорить.*", value=f"Модератор {inter.author.mention} размутил пользователя {member.mention}.\n")
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon.url)
        await inter.send(embed=embed)
        await member.edit(timeout=None)

    # Обработка ошибок
    @unmute.error
    async def unmute_error(self, inter, error):
        if isinstance(error, commands.BotMissingPermissions):
            await inter.send("У меня недостаточно прав для выполнения этой команды!", ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            await inter.send("У вас недостаточно прав для выполнения этой команды!", ephemeral=True)

    # Команда для бана пользователя
    @commands.slash_command(name="ban", description="Забанить человека")
    async def ban(self, inter,
                  member: disnake.Member = commands.Param(name='пользователь', description="Пользователь которого нужно бана"),
                  reason: str = commands.Param("Не указана", name="причина", description="Причина бана")):
        # Проверки на наличие прав
        if member.id == inter.guild.owner_id:
            return await inter.send("Нельзя забанить владельца сервера", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Ваша роль ниже роли пользователя, которого Вы хотите забанить!", ephemeral=True)
        if member.top_role >= inter.guild.me.top_role:
            return await inter.send("Моя роль ниже роли пользователя, которого Вы хотите забанить!", ephemeral=True)
        if member.id == self.bot.user.id:
            return await inter.send("Нельзя забанить меня!", ephemeral=True)
        
        # Бан пользователя
        embed = disnake.Embed(
            title="Бан",
            description="",
            color=0x2b2d31
        )
        embed.add_field(name="*Прощай навсегда!*", value=f"Модератор {inter.author.mention} забанил пользователя {member.mention}.\n"
                                            f"Причина: {reason}", inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon.url)
        await member.ban(reason=reason)
        await inter.send(embed=embed)
        

    # Обработка ошибок
    @ban.error
    async def ban_error(self, inter, error):
        if isinstance(error, commands.BotMissingPermissions):
            await inter.send("У меня недостаточно прав для выполнения этой команды!", ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            await inter.send("У вас недостаточно прав для выполнения этой команды!", ephemeral=True)

    # Команда для кика пользователя
    @commands.slash_command(name="kick", description="Кикнуть человека")
    async def kick(self, inter,
                   member: disnake.Member = commands.Param(name='пользователь', description="Пользователь которого нужно кикнуть"),
                   reason: str = commands.Param("Не указана", name="причина", description="Причина кика")):
        # Проверки на наличие прав
        if member.id == inter.guild.owner_id:
            return await inter.send("Нельзя кикнуть владельца сервера", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Ваша роль ниже роли пользователя, которого Вы хотите кикнуть!", ephemeral=True)
        if member.top_role >= inter.guild.me.top_role:
            return await inter.send("Моя роль ниже роли пользователя, которого Вы хотите кикнуть!", ephemeral=True)
        if member.id == self.bot.user.id:
            return await inter.send("Нельзя кикнуть меня!", ephemeral=True)
        
        # Кик пользователя
        embed = disnake.Embed(
            title="Кик",
            description="",
            color=0x2b2d31
        )
        embed.add_field(name="*Прощай!*", value=f"Модератор {inter.author.mention} кикнул пользователя {member.mention}.\n"
                                            f"Причина: {reason}", inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=inter.guild.name, icon_url=inter.guild.icon.url)
        await member.kick(reason=reason)
        await inter.send(embed=embed)

    
    # Обработка ошибок
    @kick.error
    async def kick_error(self, inter, error):
        if isinstance(error, commands.BotMissingPermissions):
            await inter.send("У меня недостаточно прав для выполнения этой команды!", ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            await inter.send("У вас недостаточно прав для выполнения этой команды!", ephemeral=True)

    # Команда для очистки сообщений
    @commands.slash_command(name="clear", description="Очистить сообщения")
    async def clear(self, inter,
                    amount: int = commands.Param(name='количество', description="Количество сообщений для удаления")):
        # Проверка на наличие прав
        if amount > 100:
            return await inter.send("Нельзя удалить больше 100 сообщений!", ephemeral=True)
        if amount < 1:
            return await inter.send("Нельзя удалить меньше 1 сообщения!", ephemeral=True)

        try:# Очистка сообщений
            await inter.channel.purge(limit=amount + 1)
            await inter.send(f"Удалено {amount} сообщений!", ephemeral=True)
        except Exception as e:
            await inter.send(f"Произошла какая то ошибка! Код ошибки: ```{e}```, передайте ее разработчику!")

    # Обработка ошибок
    @clear.error
    async def clear_error(self, inter, error):
        if isinstance(error, commands.BotMissingPermissions):
            await inter.send("У меня недостаточно прав для выполнения этой команды!", ephemeral=True)
        if isinstance(error, commands.MissingPermissions):
            await inter.send("У вас недостаточно прав для выполнения этой команды!", ephemeral=True)


def setup(bot):
    bot.add_cog(Mod(bot))
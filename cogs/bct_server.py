import disnake
from disnake.ext import commands, components

class BCTeam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @components.button_listener()
    async def but_listener(self, inter: disnake.MessageInteraction):
        member = inter.guild.get_member(inter.author.id)
        role = inter.guild.get_role(1184727496801931325)
        await member.add_roles(role)
        await inter.send(f"Добро пожаловать на сервер, <@{inter.author.id}>")
        channel = self.bot.get_channel(1184733956516626452)
        embed = disnake.Embed(
            title="Встречайте!",
            description=f"Поприветствуйте <@{inter.author.id}>!"
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

    @components.select_listener()
    async def notif_listener(self, inter: disnake.MessageInteraction, selected: str = components.SelectValue("Выбирай тут!")):
        botupd_role = 1184727449733439568
        servupd_role = 1184727551814418472
        member = inter.guild.get_member(inter.author.id)
        if selected == "bot_upd":
            if botupd_role in member.roles:
                await member.remove_roles(botupd_role)
                await inter.send(f"Роль <@&{botupd_role}> успешно убрана", ephemeral=True)
            else:
                await member.add_roles(botupd_role)
                await inter.send(f"Роль <@&{botupd_role}> успешно вам выдана", ephemeral=True)
        if selected == "serv_upd":
            if servupd_role in member.roles:
                await member.remove_roles(servupd_role)
                await inter.send(f"Роль <@&{servupd_role}> успешно убрана", ephemeral=True)
            else:
                await member.add_roles(servupd_role)
                await inter.send(f"Роль <@&{servupd_role}> успешно вам выдана", ephemeral=True)
            
    @components.button_listener()
    async def verif_listener(self, inter: disnake.MessageInteraction):
        auth_options = [
            disnake.SelectOption(label='bot_upd', value='Новости бота!'),
            disnake.SelectOption(label='serv_upd', value='Новости сервера!')
        ]
        select = disnake.ui.Select(
            placeholder="Выбирайте тут!",
            options=auth_options,
            custom_id=await self.notif_listener.build_custom_id(),
        )
        but = disnake.ui.Button(
            label = "Закончить",
            custom_id = await self.but_listener.build_custom_id()
        )
        await inter.send("Какие уведомления вы хотите получать?\nПосле выбора нажмите на кнопку закончить", components = [select, but], ephemeral=True)

    @commands.command()
    @commands.is_owner()
    async def verif(self, inter: disnake.MessageInteraction):
        await inter.send("Перед вступлением на сервере пожалуйста прочитайте этот канал, а так же канал <#1184721731332616344>\nЕсли вы прочитали всю информацию, нажмите на кнопку ниже.", components = disnake.ui.Button(
            label="✅",
            custom_id=await self.verif_listener.build_custom_id()
        ))

    @commands.command()
    @commands.is_owner()
    async def role_sel(self, inter: disnake.MessageInteraction):
        auth_options = [
            disnake.SelectOption(label='bot_upd', value='Новости бота!'),
            disnake.SelectOption(label='serv_upd', value='Новости сервера!')
        ]
        select = disnake.ui.Select(
            placeholder="Выбирайте тут!",
            options=auth_options,
            custom_id=await self.notif_listener.build_custom_id(),
        )
        await inter.send("Какие уведомления вы хотите получать?\nПосле выбора нажмите на кнопку закончить", components = select)

def setup(bot: commands.Bot):
    bot.add_cog(BCTeam(bot))

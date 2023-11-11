import disnake
from disnake.ext import commands, components

class DbdTeam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @components.select_listener()
    async def auth_listener(self, inter: disnake.MessageInteraction, selected: str = components.SelectValue("На каком языке вы говорите? | What language do you speak?")):
        if selected == "RU":
            await inter.response.send_message("ты русский", ephemeral=True)
        elif selected == "EN":
            await inter.response.send_message("ты англичанин", ephemeral=True)

    @components.button_listener()
    async def auth_listener(self, inter: disnake.MessageInteraction):
        auth_options = [
            disnake.SelectOption(label='RU', value='RU'),
            disnake.SelectOption(label='EN', value='EN')
        ]
        select = disnake.ui.Select(
            placeholder="На каком языке вы говорите? | What language do you speak?",
            options=auth_options,
            custom_id=await self.auth_select(),
        )

        embed = disnake.Embed(title="Language Selection")
        await inter.response.send_message(embed=embed, components=select, ephemeral=True)

    @commands.command()
    async def auth_menu(self, inter):
        embed = disnake.Embed(
            title="Информация о сервере | Server information",
            description="",
            color=0x2F3136,
        )
        embed.add_field(
            name="Общая | General",
            value=":flag_ru: Наш сервер мультиязычный, чтобы получить доступ к категории вашего языка, пройдите опрос ниже.\n:flag_us: Our server is multilingual, to get access to the category of your language, take the survey below.",
            inline=False,
        )
        embed.add_field(
            name="Правила | Rules",
            value=":flag_ru: Правила нашего сервера можно прочитать в канале <#1144980069987668060>.\n:flag_us: The rules of our server can be read in the <#1144980069987668060> channel.",
        )
        embed.set_footer(
            text=":flag_ru: Нажмите на кнопку ниже, чтобы выбрать язык.\n:flag_us: Click the button below to select a language."
        )
        await inter.response.send_message(
            embed=embed,
            components=disnake.ui.Button(
                label="✅",
                custom_id=self.secret_listener.build_custom_id()
            )
        )

def setup(bot: commands.Bot):
    bot.add_cog(DbdTeam(bot))

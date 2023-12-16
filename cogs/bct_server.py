import disnake
from disnake.ext import commands, components
from random import choice



class BCTeam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @components.button_listener()
    async def verif_listener(self, inter: disnake.MessageInteraction):
        # print(inter.author.roles)
        role=inter.guild.get_role(1184727496801931325)
        phrases=[
            "Перестань жать на эту кнопку! Она тебе ничего не даст!!",
            "На что ты надеялся, нажав на эту кнопку? На чудо? Я огорчу тебя, ничего не произойдет.",
            "Ты уже прошел верификацию. Не нажимай на эту кнопку, она не даст тебе печенек, как бы ты не старался.",
            "А ты знал, что ты не сможешь сломать бота, если будешь часто нажимать на эту кнопку?",
            "Опять ты? Эта кнопка не волшебная, она не исполнит твои желания, даже если ты будешь на неё нажимать всю ночь!",
            "Ты надеялся на что-то волшебное, нажимая на эту кнопку? Извини, но я не джинн из волшебной лампы.",
            "Знаешь, частое нажатие на эту кнопку не превратит тебя в супер-пользователя. Но можешь попробовать, если не веришь.",
            "Нажимай, нажимай, но знай - это не кнопка бесконечной мудрости. И нет, она не даст тебе дополнительных жизней в игре.",
            "Ты уже прошел верификацию. Эта кнопка не машина времени, она не вернет тебя назад, чтобы ты мог пройти верификацию снова.",
            "А ты знал, что боты не устают? Так что ты можешь нажимать эту кнопку хоть до упаду, но это ничего не изменит.",
            "На что ты надеялся, нажав на эту кнопку? На бесконечное счастье? Увы, все не так просто в этом мире."
        ]
        if role in inter.author.roles:
            await inter.send(choice(phrases), ephemeral=True)
        else:
            await inter.author.add_roles(role)
            await inter.send("Вы успешно получили доступ к серверу!", ephemeral=True)

    @commands.command()
    @commands.is_owner()
    async def verif(self, inter: disnake.MessageInteraction):
        but = disnake.ui.Button(
            label="✅",
            custom_id= await self.verif_listener.build_custom_id()
        )
        await inter.send("Перед вступлением на сервере пожалуйста прочитайте этот канал, а так же канал <#1184721731332616344>\nЕсли вы прочитали всю информацию, смело нажимайте на кнопку ниже.", components=but)

    @commands.command()
    @commands.is_owner()
    async def rules(self, inter):
        embed = disnake.Embed(
        title="Правила сервера",
        description="Ознакомьтесь с этими правилами, чтобы обеспечить приятное общение на нашем сервере.",
        color=disnake.Color.green()
    )
        embed.add_field(name="Правило 1", value="> Будьте уважительны и дружелюбны друг к другу.", inline=False)
        embed.add_field(name="Правило 2", value="> Не спамьте и не флудите в каналах (за исключением канала <#1184728169949958194>).", inline=False)
        embed.add_field(name="Правило 3", value="> Не распространяйте неприемлемый (NSFW) или оскорбительный контент.", inline=False)
        embed.add_field(name="Правило 4", value="> Не публикуйте рекламу без разрешения администрации.", inline=False)
        embed.add_field(name="Правило 5", value="> Соблюдайте тематику каналов.", inline=False)
        embed.add_field(name="Правило 6", value="> Не распространяйте личную информацию других людей без их согласия.", inline=False)
        embed.add_field(name="", value="**Администрация в праве сами выбирать тип и время наказания для нарушителя. При заходе на данный сервер Вы автоматически соглашаетесь с правилами [ToS Discord'а](https://discord.com/terms). Без упоминания всего сервера, данные правила не будут изменяться (за исключением мелких поправок). Незнание правил не освобождает Вас от наказания. По всем вопросам писать модераторам или креатором, находящиеся в сети.**")

        await inter.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(BCTeam(bot))

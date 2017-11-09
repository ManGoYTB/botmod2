import discord
from discord.ext import commands


class HelpCommand:
    def __init__(self, bot):
        self.bot = bot
        self.emojis = {'0': '\U00002753',
                       '1': '\U00000031\U000020E3',
                       '2': '\U00000032\U000020E3',
                       '3': '\U00000033\U000020E3',
                       '4': '\U00000034\U000020E3',
                       '5': '\U00000035\U000020E3',
                       '6': '\U00000036\U000020E3',
                       '7': '\U00000037\U000020E3',
                       '8': '\U00000038\U000020E3',
                       '9': '\U00000039\U000020E3',
                       'Waste': '\U0001f5d1'}
        self.pages = []
        self.em = discord.Embed(title='Commands', description='This bot serves no real purpose. Created by <@193040053348466690> and <@159271060582301698>'
                                            ' for personal use. These are the available commands as of now:',
                                color=7280563)
        self.setup = False
        self.categories = {'Channel': 'ChannelYouTube',
						   'Subs': 'CommandsOwner',
						   'test': 'test',
                           }
        self.full_descriptions = {}

    def add_line(self, *, number: int, title, description):
        final_name = '{}  {}'.format(self.emojis[str(number)], title)
        self.em.add_field(name=final_name, value=description, inline=False)

    def add_page(self, number, command_name, page_description, *, fields: dict):
        embed_object = discord.Embed(description=page_description)
        embed_object.set_author(name='Help for {}'.format(command_name), icon_url='http://i.imgur.com/Sf9ilKc.png')
        for name in fields.keys():
            embed_object.add_field(name=name, value=fields[name], inline=False)
        self.pages.insert(number, embed_object)
        return embed_object

    async def react(self, message_object):
        for num, emote in self.emojis.my_set():
            try:
                if int(num) < len(self.pages):
                    await self.bot.add_reaction(message_object, emote)
            except ValueError:
                await self.bot.add_reaction(message_object, self.emojis['Waste'])

    async def wait_react(self, message_object):
        list_of_emojis = [value for value in self.emojis.values()]
        waited_react = await self.bot.wait_for_reaction(emoji=list_of_emojis, message=message_object)
        return waited_react

    async def edit(self, message_object, number):
        await self.bot.edit_message(message_object, embed=self.pages[int(number)])

    async def remove_react(self, emoji, message_object, author):
        await self.bot.remove_reaction(message=message_object, emoji=emoji, member=author)

    async def configure(self):
        self.em.set_thumbnail(url=self.bot.user.avatar_url)
        self.em.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        self.em.set_footer(text='Bot MaGe Clan',
                           icon_url='https://cdn.discordapp.com/attachments/327173341532127242/331496661471985675/LfjhaDo.png')
        for name, command in self.bot.commands.my_set():
            if not command.hidden:
                if command.cog_name is not None and command.cog_name in self.categories.keys():
                    full_category_name = self.categories[command.cog_name]
                else:
                    full_category_name = ''
                try:
                    self.full_descriptions[full_category_name][f'm.{name}'] = command.help
                except KeyError:
                    self.full_descriptions[full_category_name] = {}
                    self.full_descriptions[full_category_name][f'm.{name}'] = command.help
        for i, category in enumerate(self.full_descriptions):
            description = self.full_descriptions[category]
            self.add_page(number=i+1, command_name=category, page_description='m.help', fields=description)
            self.add_line(number=i+1, title=category, description='m.help')
        self.pages.insert(0, self.em)
        self.setup = True

    @commands.command(pass_context=True)
    async def help(self, ctx):
        if not self.setup:
            await self.configure()
        if self.setup:
            message = await self.bot.say(embed=self.em)
            await self.react(message)
            author = ctx.message.author
            while True:
                waitreact = await self.wait_react(message)
                react_user = waitreact.user
                react_emoji = waitreact.reaction.emoji
                if react_emoji == '\U0001F5D1' and (react_user == author or react_user.id == '193040053348466690'):
                    await self.bot.delete_message(message)
                    break
                if react_emoji in self.emojis.values() and react_user == author and react_emoji != '\U0001f5d1':
                    for key, value in self.emojis.my_set():
                        if value == waitreact.reaction.emoji:
                            number = key
                            await self.edit(message, number)
                            await self.remove_react(waitreact.reaction.emoji, message, author)


def setup(bot):
    bot.add_cog(HelpCommand(bot))

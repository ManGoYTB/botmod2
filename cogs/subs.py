import discord
from discord.ext import commands
import asyncio
import json
from .check import checks
import aiohttp


class Subs:
    def __init__(self, bot):
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        self.bot = bot
        self.numbers = {'1': ':one:',
                        '2': ':two:',
                        '3': ':three:',
                        '4': ':four:',
                        '5': ':five:',
                        '6': ':six:',
                        '7': ':seven:',
                        '8': ':eight:',
                        '9': ':nine:',
                        '0': ':zero:'}
        self.sub_count = 0
        self.confirm = True
        self.double_instance = False
        self.interval = 10

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def startsubs(self, ctx):
        if not self.double_instance:
            await self.bot.say('Instance started.')
            while True:
                self.double_instance = True
                parameters = {"id": "UCnFHsZfaCwgBzbmt89Nmj3A",
                              "key": "AIzaSyCssyjjfIcJpvl4CYoD20LbKcWIxQPNvw8",
                              "part": "statistics",
                              "fields": "items/statistics/subscriberCount"}
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.googleapis.com/youtube/v3/channels", params=parameters) as r:
                            json_data = await r.json()
                sub_count = json_data['items'][0]['statistics']['subscriberCount']
                if sub_count != self.sub_count:
                    self.sub_count = sub_count
                    text = ''.join([self.numbers[x] for x in sub_count if x in self.numbers.keys()])
                    await self.bot.edit_channel(ctx.message.channel, topic=' **Total Subscribers** __**MaGe Clan**__ : {} __**bit.ly/MaGeClan**__<:xd:312128955467431936>'.format(text))
                if not self.confirm:
                    await self.bot.say('Done')
                    break
                await asyncio.sleep(self.interval)
        elif self.double_instance:
            await self.bot.say('An instance of the live subscriber counter is already running.')

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def new(self,ctx):
        embed=discord.Embed(
            title="TITRE",
            color=0x180776,
            description="DESCRIPTION")
        embed.set_author(name="Update", icon_url='https://images-ext-1.discordapp.net/external/ygp_PwF-i3O3ib5wjG30lkCAW-Xshf2Bxx5JUFVzcXI/https/yt3.ggpht.com/-CRZ_NLhRUEs/AAAAAAAAAAI/AAAAAAAAAAA/sDANm7rogzE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg?width=80&height=80')
        embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/2dZVVL6feMSM7lxfFkKVW__LToSOzmToSEmocJV5vcA/https/cdn.discordapp.com/embed/avatars/0.png?width=80&height=80')
        embed.set_footer(text="DATE")
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)

def setup(bot):
    bot.add_cog(Subs(bot))

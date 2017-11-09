import aiohttp
from discord.ext import commands
import discord

class Subss:
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        # self.message = '**{}** Subscribers|Subscribe  -> :link: __**https://www.youtube.com/channel/UCzVdft7CxIu-SbZxR716UcQ**__ '

    def subs_emb(self, subs):
        emb = discord.Embed(title="**{}** Subscribers|Subscribe 👇".format(subs),
                            description="🔗 **[ClickHere](https://www.youtube.com/channel/UCzVdft7CxIu-SbZxR716UcQ)**<:kk:332133470572642317><:kiki:332139133461987329>",
                            color=0xc56567)
        emb.set_author(name="Kifkif59", url="https://www.youtube.com/channel/UCzVdft7CxIu-SbZxR716UcQ", icon_url="https://yt3.ggpht.com/-l5VUiWvdje8/AAAAAAAAAAI/AAAAAAAAAAA/SX00dn2m8SE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        emb.set_thumbnail(url='https://yt3.ggpht.com/-l5VUiWvdje8/AAAAAAAAAAI/AAAAAAAAAAA/SX00dn2m8SE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg')
        emb.set_footer(text="Kifkif59", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        return emb

    @commands.command(pass_context=True)
    async def subskifkif(self, ctx):
        parameters = {"id": "UCzVdft7CxIu-SbZxR716UcQ", "key": "AIzaSyCssyjjfIcJpvl4CYoD20LbKcWIxQPNvw8", "part": "statistics",
                      "fields": "items/statistics/subscriberCount"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/youtube/v3/channels", params=parameters) as r:
                if r.status == 200:
                    json_data = await r.json()
                    sub_count = json_data['items'][0]['statistics']['subscriberCount']
                    await self.bot.send_message(ctx.message.channel, embed=self.subs_emb(sub_count))
                else:
                    await self.bot.say('Error: Status {}, contact the creator'.format(r.status))


def setup(bot):
    bot.add_cog(Subss(bot))
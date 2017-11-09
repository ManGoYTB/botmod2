import aiohttp
from discord.ext import commands
import discord

class Subss:
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
        # self.message = '**{}** Subscribers|Subscribe  -> :link: __**https://www.youtube.com/channel/UCdBgaPUcYkOEooVlV5rxrXw**__ '

    def subs_emb(self, subs):
        emb = discord.Embed(title="**{}** Subscribers|Subscribe 👇".format(subs),
                            description="🔗 **[ClickHere](https://www.youtube.com/channel/UCdBgaPUcYkOEooVlV5rxrXw)**<:kk:332133470572642317><:abdel:332139225107660802>",
                            color=0x9e30c2)
        emb.set_author(name="Abdel64", url="https://www.youtube.com/channel/UCdBgaPUcYkOEooVlV5rxrXw", icon_url="https://yt3.ggpht.com/-8JmQnUV5SU0/AAAAAAAAAAI/AAAAAAAAAAA/iXdHsJl4X3M/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        emb.set_thumbnail(url='https://yt3.ggpht.com/-8JmQnUV5SU0/AAAAAAAAAAI/AAAAAAAAAAA/iXdHsJl4X3M/s100-c-k-no-mo-rj-c0xffffff/photo.jpg')
        emb.set_footer(text="Abdel64", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        return emb

    @commands.command(pass_context=True)
    async def subsabdel(self, ctx):
        parameters = {"id": "UCdBgaPUcYkOEooVlV5rxrXw", "key": "AIzaSyCssyjjfIcJpvl4CYoD20LbKcWIxQPNvw8", "part": "statistics",
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
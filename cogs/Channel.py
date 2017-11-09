import discord
from discord.ext import commands

class Channel:
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def ytmango(self,ctx):
        """YouTube ManGoYT"""
        embed = discord.Embed(
            title="**YouTube ManGoYT**<:ManGoYT:299207412907245569> <:youtube:329991214327660544><:croown:336916788703133707> :",
            color=0x2626f0,
            description="<:PI:309724535148511242>**https://www.youtube.com/c/ManGoYTB**<:pp:332133471877070848> ```\nLeader MaGeClan``` ")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-CRZ_NLhRUEs/AAAAAAAAAAI/AAAAAAAAAAA/sDANm7rogzE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")    
        embed.set_author(name="ManGoYT", url="https://www.youtube.com/c/ManGoYTB", icon_url="https://yt3.ggpht.com/-CRZ_NLhRUEs/AAAAAAAAAAI/AAAAAAAAAAA/sDANm7rogzE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        embed.add_field(name="<:FS:309728585709649920>", value="<:croown:336916788703133707>", inline=True)
        embed.set_footer(text="ManGoYT", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.add_field(name="<:STAFF:329991353700319233>", value="<:omgtroll:299208059685961728>", inline=True)
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)

    @commands.command(pass_context=True)
    async def ytmage(self,ctx):
        """YouTube MaGe Clan"""
        embed = discord.Embed(
            title="**YouTube MaGe Clan**<:youtube:329991214327660544> <:youtube:329991214327660544>:",
            color=0xf0ff35,
            description="<:PI:309724535148511242>**https://www.youtube.com/channel/UCnFHsZfaCwgBzbmt89Nmj3A**<:pp:332133471877070848>")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-palNhXtV33c/AAAAAAAAAAI/AAAAAAAAAAA/DgJik9EDvqA/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")    
        embed.set_footer(text="MaGeClan", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.set_author(name="MaGeClan", url="https://www.youtube.com/channel/UCnFHsZfaCwgBzbmt89Nmj3A", icon_url="https://yt3.ggpht.com/-palNhXtV33c/AAAAAAAAAAI/AAAAAAAAAAA/DgJik9EDvqA/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")        
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)		

    @commands.command(pass_context=True)
    async def ytabdel(self,ctx):
        """YouTube Abdel64"""
        embed = discord.Embed(
            title="**YouTube Abdel64**<:youtube:329991214327660544> <:youtube:329991214327660544>:",
            color=0x9e30c2,
            description="<:PI:309724535148511242>**https://www.youtube.com/channel/UCdBgaPUcYkOEooVlV5rxrXw**<:pp:332133471877070848>")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-8JmQnUV5SU0/AAAAAAAAAAI/AAAAAAAAAAA/iXdHsJl4X3M/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        embed.set_footer(text="Abdel64", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.set_author(name="Abdel64", url="https://www.youtube.com/channel/UCdBgaPUcYkOEooVlV5rxrXw", icon_url="https://yt3.ggpht.com/-8JmQnUV5SU0/AAAAAAAAAAI/AAAAAAAAAAA/iXdHsJl4X3M/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")        
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed) 	

    @commands.command(pass_context=True)
    async def ytray(self,ctx):
        """YouTube Ray"""
        embed = discord.Embed(
            title="**YouTube Ray**<:youtube:329991214327660544> <:youtube:329991214327660544>:",
            color=0x930003,
            description="<:PI:309724535148511242>**https://www.youtube.com/channel/UCyGpuvdM27Lfi4lzSgdY9eA**<:pp:332133471877070848>")
        embed.set_footer(text="Ray", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-UqJIQBQ6o5Q/AAAAAAAAAAI/AAAAAAAAAAA/cnNVA1EX5L4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")    
        embed.set_author(name="Ray", url="https://www.youtube.com/channel/UCyGpuvdM27Lfi4lzSgdY9eA", icon_url="https://yt3.ggpht.com/-UqJIQBQ6o5Q/AAAAAAAAAAI/AAAAAAAAAAA/cnNVA1EX5L4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)  

    @commands.command(pass_context=True)
    async def ytkifkif(self,ctx):
        """YouTube Kifkif"""
        embed = discord.Embed(
            title="**YouTube Kifkif**<:youtube:329991214327660544> <:youtube:329991214327660544>:",
            color=0xc56567,
            description="<:PI:309724535148511242>**https://www.youtube.com/channel/UCzVdft7CxIu-SbZxR716UcQ**<:pp:332133471877070848>")
        embed.set_footer(text="Kifkif59", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-l5VUiWvdje8/AAAAAAAAAAI/AAAAAAAAAAA/SX00dn2m8SE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        embed.set_author(name="Kifkif", url="https://www.youtube.com/channel/UCzVdft7CxIu-SbZxR716UcQ", icon_url="https://yt3.ggpht.com/-l5VUiWvdje8/AAAAAAAAAAI/AAAAAAAAAAA/SX00dn2m8SE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)

    @commands.command(pass_context=True)
    async def ytreaper(self,ctx):
        """YouTube The Reaper"""
        embed = discord.Embed(
            title="**YouTube The Reaper**<:youtube:329991214327660544> <:youtube:329991214327660544>:",
            color=0x2626f0,
            description="<:PI:309724535148511242>**https://www.youtube.com/channel/UCiJMqxVi_vSVbIcuGwVQybg**<:pp:332133471877070848>")
        embed.set_footer(text="The Reaper", icon_url="https://cdn.discordapp.com/emojis/329991214327660544.png")
        embed.set_thumbnail(url="https://yt3.ggpht.com/-MpWlOugIa0U/AAAAAAAAAAI/AAAAAAAAAAA/FsRxyfe8Fxo/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        embed.set_author(name="The Reaper", url="https://www.youtube.com/channel/UCiJMqxVi_vSVbIcuGwVQybg", icon_url="https://yt3.ggpht.com/-MpWlOugIa0U/AAAAAAAAAAI/AAAAAAAAAAA/FsRxyfe8Fxo/s100-c-k-no-mo-rj-c0xffffff/photo.jpg")
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)		
        
def setup(bot):
    bot.add_cog(Channel(bot))
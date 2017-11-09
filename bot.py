'''
MIT License

Copyright (c) 2017 ManGo
'''

GUILD_ID = 0 # your guild id here

import discord
from discord.ext import commands
from urllib.parse import urlparse
import asyncio
import textwrap
import datetime
import time
import json
import sys
import os
import re
import string
import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import aiohttp

class Modmail(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_pre)
        self.uptime = datetime.datetime.utcnow()
        self._add_commands()
        def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _member_has_role(self, member: discord.Member, role: discord.Role):
        return role in member.roles

    def _add_commands(self):
        '''Adds commands automatically'''
        for attr in dir(self):
            cmd = getattr(self, attr)
            if isinstance(cmd, commands.Command):
                self.add_command(cmd)

    @property
    def token(self):
        '''Returns your token wherever it is'''
        try:
            with open('config.json') as f:
                config = json.load(f)
                if config.get('TOKEN') == "your_token_here":
                    if not os.environ.get('TOKEN'):
                        self.run_wizard()
                else:
                    token = config.get('TOKEN').strip('\"')
        except FileNotFoundError:
            token = None
        return os.environ.get('TOKEN') or token
    
    @staticmethod
    async def get_pre(bot, message):
        '''Returns the prefix.'''
        with open('config.json') as f:
            prefix = json.load(f).get('PREFIX')
        return os.environ.get('PREFIX') or prefix or 'm.'

    @staticmethod
    def run_wizard():
        '''Wizard for first start'''
        print('------------------------------------------')
        token = input('Enter your token:\n> ')
        print('------------------------------------------')
        data = {
                "TOKEN" : token,
            }
        with open('data/config.json','w') as f:
            f.write(json.dumps(data, indent=4))
        print('------------------------------------------')
        print('Restarting...')
        print('------------------------------------------')
        os.execv(sys.executable, ['python'] + sys.argv)

    @classmethod
    def init(cls, token=None):
        '''Starts the actual bot'''
        bot = cls()
        if token:
            to_use = token.strip('"')
        else:
            to_use = bot.token.strip('"')
        try:
            bot.run(to_use, reconnect=True)
        except Exception as e:
            raise e

    async def on_connect(self):
        print('---------------')
        print('Modmail connected!')

    @property
    def guild_id(self):
        from_heroku = os.environ.get('GUILD_ID')
        return int(from_heroku) if from_heroku else GUILD_ID

    async def on_ready(self):
        '''Bot startup, sets uptime.'''
        self.guild = discord.utils.get(self.guilds, id=self.guild_id)
        print(textwrap.dedent(f'''
        ---------------
        Client is ready!
        ---------------
        Author: ManGo#7532
        ---------------
        Logged in as: {self.user}
        User ID: {self.user.id}
        ---------------
        '''))

    def overwrites(self, ctx, modrole=None):
        '''Permision overwrites for the guild.'''
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        if modrole:
            overwrites[modrole] = discord.PermissionOverwrite(read_messages=True)
        else:
            for role in self.guess_modroles(ctx):
                overwrites[role] = discord.PermissionOverwrite(read_messages=True)

        return overwrites

    def help_embed(self):
        em = discord.Embed(color=0x00FFFF)
        em.set_author(name='Mod Mail - Help', icon_url=self.user.avatar_url)
        em.description = 'This bot is a python implementation by **ManGo**'
                 

        cmds = '`m.setup [modrole] <- (optional)` - Command that sets up the bot.\n' \
               '`m.reply <message...>` - Sends a message to the current thread\'s recipient.\n' \
               '`m.close` - Closes the current thread and deletes the channel.\n' \
               '`m.disable` - Closes all threads and disables modmail for the server.\n' \
               '`m.customstatus` - Sets the Bot status to whatever you want.'

        warn = 'Do not manually delete the category or channels as it will break the system. ' \
               'Modifying the channel topic will also break the system.'
        em.add_field(name='Commands', value=cmds)
        em.add_field(name='Warning', value=warn)
        em.add_field(name='Owner ManGo', value='ManGo#7532')
        em.set_footer(text='Star the repository to unlock hidden features!')

        return em

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx, *, modrole: discord.Role=None):
        '''Sets up a server for modmail'''
        if discord.utils.get(ctx.guild.categories, name='Mod Mail'):
            return await ctx.send('This server is already set up.')

        categ = await ctx.guild.create_category(
            name='Mod Mail', 
            overwrites=self.overwrites(ctx, modrole=modrole)
            )
        await categ.edit(position=0)
        c = await ctx.guild.create_text_channel(name='bot-info', category=categ)
        await c.edit(topic='Manually add user id\'s to block users.\n\n'
                           'Blocked\n-------\n\n')
        await c.send(embed=self.help_embed())
        await ctx.send('Successfully set up server.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):
        '''Close all threads and disable modmail.'''
        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        if not categ:
            return await ctx.send('This server is not set up.')
        for category, channels in ctx.guild.by_category():
            if category == categ:
                for chan in channels:
                    if 'User ID:' in str(chan.topic):
                        user_id = int(chan.topic.split(': ')[1])
                        user = self.get_user(user_id)
                        await user.send(f'**{ctx.author}** has closed this modmail session.')
                    await chan.delete()
        await categ.delete()
        await ctx.send('Disabled modmail.')


    @commands.command(name='close')
    @commands.has_permissions(manage_guild=True)
    async def _close(self, ctx):
        '''Close the current thread.'''
        if 'User ID:' not in str(ctx.channel.topic):
            return await ctx.send('This is not a modmail thread.')
        user_id = int(ctx.channel.topic.split(': ')[1])
        user = self.get_user(user_id)
        em = discord.Embed(title='Thread Closed')
        em.description = f'**{ctx.author}** has closed this modmail session.'
        em.color = discord.Color.red()
        try:
            await user.send(embed=em)
        except:
            pass
        await ctx.channel.delete()

    @commands.command()
    async def ping(self, ctx):
        """Pong! Returns your websocket latency."""
        em = discord.Embed()
        em.title ='Pong! Websocket Latency:'
        em.description = f'{self.ws.latency * 1000:.4f} ms'
        em.color = 0x00FF00
        await ctx.send(embed=em)

    def guess_modroles(self, ctx):
        '''Finds roles if it has the manage_guild perm'''
        for role in ctx.guild.roles:
            if role.permissions.manage_guild:
                yield role

    def format_info(self, user):
        '''Get information about a member of a server
        supports users from the guild or not.'''
        server = self.guild
        member = self.guild.get_member(user.id)
        avi = user.avatar_url
        time = datetime.datetime.utcnow()
        desc = 'Modmail thread started.'
        color = 0

        if member:
            roles = sorted(member.roles, key=lambda c: c.position)
            rolenames = ', '.join([r.name for r in roles if r.name != "@everyone"]) or 'None'
            member_number = sorted(server.members, key=lambda m: m.joined_at).index(member) + 1
            for role in roles:
                if str(role.color) != "#000000":
                    color = role.color

        em = discord.Embed(colour=color, description=desc, timestamp=time)

        em.add_field(name='Account Created', value=str((time - user.created_at).days)+' days ago.')
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url=server.icon_url)

        if member:
            em.add_field(name='Joined', value=str((time - member.joined_at).days)+' days ago.')
            em.add_field(name='Member No.',value=str(member_number),inline = True)
            em.add_field(name='Nick', value=member.nick, inline=True)
            em.add_field(name='Roles', value=rolenames, inline=True)

        return em

    async def send_mail(self, message, channel, mod):
        author = message.author
        fmt = discord.Embed()
        fmt.description = message.content
        fmt.timestamp = message.created_at

        urls = re.findall(r'(https?://[^\s]+)', message.content)

        types = ['.png', '.jpg', '.gif', '.jpeg', '.webp']

        for u in urls:
            if any(urlparse(u).path.endswith(x) for x in types):
                fmt.set_image(url=u)
                break

        if mod:
            fmt.color=discord.Color.green()
            fmt.set_author(name=str(author), icon_url=author.avatar_url)
            fmt.set_footer(text='Moderator')
        else:
            fmt.color=discord.Color.gold()
            fmt.set_author(name=str(author), icon_url=author.avatar_url)
            fmt.set_footer(text='User')

        embed = None

        if message.attachments:
            fmt.set_image(url=message.attachments[0].url)

        await channel.send(embed=fmt)

    async def process_reply(self, message):
        try:
            await message.delete()
        except discord.errors.NotFound:
            pass
        await self.send_mail(message, message.channel, mod=True)
        user_id = int(message.channel.topic.split(': ')[1])
        user = self.get_user(user_id)
        await self.send_mail(message, user, mod=True)

    def format_name(self, author):
        name = author.name
        new_name = ''
        for letter in name:
            if letter in string.ascii_letters + string.digits:
                new_name += letter
        if not new_name:
            new_name = 'null'
        new_name += f'-{author.discriminator}'
        return new_name

    @property
    def blocked_em(self):
        em = discord.Embed(title='Message not sent!', color=discord.Color.red())
        em.description = 'You have been blocked from using modmail.'
        return em

    async def process_modmail(self, message):
        '''Processes messages sent to the bot.'''
        try:
            await message.add_reaction('✅')
        except:
            pass

        guild = self.guild
        author = message.author
        topic = f'User ID: {author.id}'
        channel = discord.utils.get(guild.text_channels, topic=topic)
        categ = discord.utils.get(guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        blocked = top_chan.topic.split('Blocked\n-------')[1].strip().split('\n')
        blocked = [x.strip() for x in blocked]

        if str(message.author.id) in blocked:
            return await message.author.send(embed=self.blocked_em)

        em = discord.Embed(title='Thanks for the message!')
        em.description = 'The moderation team will get back to you as soon as possible!'
        em.color = discord.Color.green()

        if channel is not None:
            await self.send_mail(message, channel, mod=False)
        else:
            await message.author.send(embed=em)
            channel = await guild.create_text_channel(
                name=self.format_name(author),
                category=categ
                )
            await channel.edit(topic=topic)
            await channel.send('@here', embed=self.format_info(author))
            await channel.send('\u200b')
            await self.send_mail(message, channel, mod=False)

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)
        if isinstance(message.channel, discord.DMChannel):
            await self.process_modmail(message)

    @commands.command()
    async def reply(self, ctx, *, msg):
        '''Reply to users using this command.'''
        categ = discord.utils.get(ctx.guild.categories, id=ctx.channel.category_id)
        if categ is not None:
            if categ.name == 'Mod Mail':
                if 'User ID:' in ctx.channel.topic:
                    ctx.message.content = msg
                    await self.process_reply(ctx.message)

    @commands.command(name="customstatus", aliases=['status', 'presence'])
    @commands.has_permissions(administrator=True)
    async def _status(self, ctx, *, message):
        '''Set a custom playing status for the bot.'''
        if message == 'clear':
            return await self.change_presence(game=None)
        await self.change_presence(game=discord.Game(name=message), status=discord.Status.idle)
        await ctx.send(f"Changed status to **{message}**")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def block(self, ctx, id=None):
        '''Block a user from using modmail.'''
        if id is None:
            if 'User ID:' in str(ctx.channel.topic):
                id = ctx.channel.topic.split('User ID: ')[1].strip()
            else:
                return await ctx.send('No User ID provided.')

        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        topic = str(top_chan.topic)
        topic += id + '\n'

        if id not in top_chan.topic:  
            await top_chan.edit(topic=topic)
            await ctx.send('User successfully blocked!')
        else:
            await ctx.send('User is already blocked.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unblock(self, ctx, id=None):
        '''Unblocks a user from using modmail.'''
        if id is None:
            if 'User ID:' in str(ctx.channel.topic):
                id = ctx.channel.topic.split('User ID: ')[1].strip()
            else:
                return await ctx.send('No User ID provided.')

        categ = discord.utils.get(ctx.guild.categories, name='Mod Mail')
        top_chan = categ.channels[0] #bot-info
        topic = str(top_chan.topic)
        topic = topic.replace(id+'\n', '')

        if id in top_chan.topic:
            await top_chan.edit(topic=topic)
            await ctx.send('User successfully unblocked!')
        else:
            await ctx.send('User is not already blocked.')
            
    @commands.command()
    async def info(self):
        """Shows info about Red"""
        server_url = "https://discord.gg/pcYQwmd"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.utcnow() - since).days
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        py_version = "[{}.{}.{}]({})".format(*os.sys.version_info[:3],
                                             python_url)

        owner_set = self.bot.settings.owner is not None
        owner = self.bot.settings.owner if owner_set else None
        if owner:
            owner = discord.utils.get(self.bot.get_all_members(), id=owner)
            if not owner:
                try:
                    owner = await self.bot.get_user_info(self.bot.settings.owner)
                except:
                    owner = None
        if not owner:
            owner = "Unknown"

        about = (
            "Created by ManGoYT <3 Invite your friends {} "
            "".format(server_url))

        embed = discord.Embed(colour=discord.Colour.red())
        embed.add_field(name="Instance owned by", value=str(owner))
        embed.add_field(name="Python", value=py_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name="About Red", value=about, inline=False)
        embed.set_footer(text="Bringing joy since 02 Jan 2016 (over "
                         "{} days ago!)".format(days_since))

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")
							   
    @commands.command()
    async def uptime(self):
        """Shows Red's uptime"""
        since = self.bot.uptime.strftime("%Y-%m-%d %H:%M:%S")
        passed = self.get_bot_uptime()
        await self.bot.say("Been up for: **{}** (since {} UTC)"
                           "".format(passed, since))
						   
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def servers(self, ctx):
        """Lists and allows to leave servers"""
        owner = ctx.message.author
        servers = sorted(list(self.bot.servers),
                         key=lambda s: s.name.lower())
        msg = ""
        for i, server in enumerate(servers):
            msg += "{}: {}\n".format(i, server.name)
        msg += "\nTo leave a server just type its number."

        for page in pagify(msg, ['\n']):
            await self.bot.say(page)

        while msg is not None:
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            try:
                msg = int(msg.content)
                await self.leave_confirmation(servers[msg], owner, ctx)
                break
            except (IndexError, ValueError, AttributeError):
                pass

    async def leave_confirmation(self, server, owner, ctx):
        await self.bot.say("Are you sure you want me "
                    "to leave {}? (yes/no)".format(server.name))

        msg = await self.bot.wait_for_message(author=owner, timeout=15)

        if msg is None:
            await self.bot.say("I guess not.")
        elif msg.content.lower().strip() in ("yes", "y"):
            await self.bot.leave_server(server)
            if server != ctx.message.server:
                await self.bot.say("Done.")
        else:
            await self.bot.say("Alright then.")
			
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def rainbow(self, ctx, interval:float, *, role):
        roleObj = discord.utils.find(lambda r: r.name == role, ctx.message.server.roles)
        if not roleObj:
            no = discord.Embed(title="{} is not a valid role".format(role))
            await self.bot.say(embed=no)
            return
        if interval < 3:
            interval = 3
        while True:
            colour = ''.join([choice('0123456789ABCDEF') for x in range(6)])
            colour = int(colour, 16)
            await self.bot.edit_role(ctx.message.server, roleObj, colour=discord.Colour(value=colour))
            await asyncio.sleep(interval)
			
    @commands.command(pass_context=True)
    async def discord(self,ctx):
        """DiscordForum"""
        embed = discord.Embed(
            title="**HelpMe**",
            color=0x7691eb,
            description="**getting started**")
        embed.set_thumbnail(url="http://www.ethicon.com/sites/all/themes/ethicon/img/ajax-loader.gif")    
        embed.set_author(name="DiscordHelp", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
        embed.add_field(name="🇫🇷👈👇", value="🔥**https://support.discordapp.com/hc/fr**🔥", inline=False)
        embed.add_field(name="🇺🇸👈👇", value="🔥**https://support.discordapp.com/hc/en-us**🔥", inline=False)
        embed.add_field(name="🇩🇪👈👇", value="🔥**https://support.discordapp.com/hc/de**🔥", inline=False)
        embed.add_field(name="🇪🇸👈👇", value="🔥**https://support.discordapp.com/hc/es**🔥", inline=False)
        embed.add_field(name="🇮🇹👈👇", value="🔥**https://support.discordapp.com/hc/it**🔥", inline=False)
        await self.bot.send_message(discord.Object(ctx.message.channel.id), embed=embed)
		
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def _mdm(self, ctx: commands.Context, *, message: str):
        """Sends a DM to all Members with the given Role.
        Allows for the following customizations:
        {0} is the member being messaged.
        {1} is the role they are being message through.
        {2} is the person sending the message.
        """

        server = ctx.message.server
        sender = ctx.message.author

        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass

        dm_these = self._get_users_with_role(server, role)

        for user in dm_these:
            try:
                await self.bot.send_message(user,
                                            message.format(user, role, sender))
            except (discord.Forbidden, discord.HTTPException):
                continue
				
if __name__ == '__main__':
    Modmail.init()

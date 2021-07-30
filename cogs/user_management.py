import discord
import requests
import json
from discord.ext import commands

class User_Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='kick', aliases=['kickuser', 'userkick'])
    @commands.guild_only()
    @commands.has_any_role('Owner', 'Co-Owner', 'Admin', 'Mod')
    async def kick(self, ctx, user: discord.Member, *, reason="No reason given."):
        if ctx.author.id == user.id:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description='You can not kick yourself...\nReally?'))
            return
        if ctx.author.top_role.id == user.top_role.id and ctx.author.id != ctx.guild.owner.id:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description='You do not have permission to do that!'))
            return
        await ctx.guild.kick(user, reason=reason)
        kick_embed = discord.Embed(
            color=discord.Color.blue(),
            description=f"User **{str(user)}** has been kicked for {reason}.")
        await ctx.send(embed=kick_embed)
    
    @commands.command(name='ban', aliases=['banuser', 'userban'])
    @commands.guild_only()
    @commands.has_any_role('Owner', 'Co-Owner', 'Admin')
    async def ban(self, ctx, user: discord.Member, *, reason="No reason given."):
        if ctx.author.id == user.id:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description='You can not ban yourself...\nReally?'))
            return
        if ctx.author.top_role.id == user.top_role.id and ctx.author.id != ctx.guild.owner.id:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description='You do not have permission to do that!'))
            return
        await ctx.guild.ban(user, reason=reason)
        ban_embed = discord.Embed(
            color=discord.Color.blue(),
            description=f"User **{str(user)}** has been banned for {reason}.")
        await ctx.send(embed=ban_embed)
        
    
    @commands.command(name="pardon", aliases=['p', 'removeban'])
    @commands.guild_only()
    @commands.has_any_role('Owner', 'Co-Owner', 'Admin')
    async def unban(self, ctx, user: discord.User, *, reason="No reason given."):
        if ctx.author.id == user.id:
            await ctx.send(embed=dicord.Embed(color=discord.Color.blue(), description='You can not pardon yourself\nReally?'))
            return
        for entry in await ctx.guild.bans():
            if entry[1].id == user.id:
                await ctx.guild.unban(user, reason=reason)
                unban_embed = discord.Embed(
                    color=discord.Color.blue(),
                    description=f'User **{str(user)}** has been unbanned\nReason: {reason}')
                await ctx.send(embed=unban_embed)
                return

        not_banned_embed = discord.Embed(
            color=discord.Color.blue(),
            description='That user has not been banned before.')
        await ctx.send(embed=not_banned_embed)


#Test in progress work for me you cunt bag https is not required but it may force https when connecting.
#I need to investigate more...?
    @commands.command(name="ip", aliases=['whois'])
    @commands.guild_only()
    @commands.has_any_role('Owner', 'Co-Owner')
    async def ip(self, ctx):
        req = requests.get('http://ip-api.com/json/99.182.185.192')
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'], resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)


def setup(client):
    client.add_cog(User_Management(client))
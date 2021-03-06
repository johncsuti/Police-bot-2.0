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
        
    
    @commands.command(name="pardon", aliases=['removeban'])
    @commands.guild_only()
    @commands.has_any_role('Owner', 'Co-Owner', 'Admin')
    async def unban(self, ctx, user: discord.User, *, reason="No reason given."):
        if ctx.author.id == user.id:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description='You can not pardon yourself\nReally?'))
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


    @commands.command(name="ip")
    @commands.guild_only()
    async def ip(self, ctx, address):
        req = requests.get(f'http://ip-api.com/json/{address}?fields=25337')
        resp = json.loads(req.content.decode())

        if req.status_code == 200:
            if resp['status'] == 'success':
                txt_data = [
                ('IP', 'query'),
                ('City', 'city'),
                ('State', 'regionName'),
                ('ZIP', 'zip'),
                ('Country', 'country'),
                ('Latitude', 'lat'),
                ('Longitude', 'lon'),
                ('ISP', 'isp')
                ]
 
                ip_embed = discord.Embed(title=f"Whois data for {address}", color=discord.Color.blue())
                for txt, key in txt_data:
                    ip_embed.add_field(name=txt, value=resp.get(key, 'Unknown'), inline=False)
                await ctx.send(embed=ip_embed)

            elif resp['status'] == 'fail':
                await ctx.send('Status: Fail')

        else:
            print('HTTP Request Failed')
            await ctx.send('HTTP Request Failed: Error {}'.format(req.status_code))

    @commands.command(name="whois")
    @commands.guild_only()
    async def whois(self, ctx, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = ctx.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.blue(), timestamp=ctx.message.created_at,
            title=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}")

        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Display Name:", value=member.display_name)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(User_Management(client))
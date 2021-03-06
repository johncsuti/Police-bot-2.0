import discord
from discord.ext import commands

class Server_Management(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Owner', 'Co-Owner', 'Admin')
    @commands.guild_only()
    async def clear(self, ctx, amount: int):

        if amount <= 10000:
            try:
                await ctx.channel.purge(limit=amount+1)
            except Exception:
                error_embed = discord.Embed(
                    color=discord.Color.blue(),
                    description='''Can't remove messages, you must be Admin or higher to perform this command.''')
                await ctx.send(embed=error_embed)
        else:
            limit_embed = discord.Embed(
                color=discord.Color.blue(),
                description='''You can't purge more then 10,000 messages at a time!\n Thanks Discord...''')
            await ctx.send(embed=limit_embed)

    @commands.Cog.listener("on_message")
    async def notalking(self, ctx):
        if str(ctx.channel) == "memes":
            if str(ctx.content).startswith('http'):
                return
            if ctx.content == "":
                return
            if ctx.content != "":
                await ctx.channel.purge(limit=1)

def setup(client):
    client.add_cog(Server_Management(client))
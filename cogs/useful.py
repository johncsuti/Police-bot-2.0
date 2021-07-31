import discord
from discord.ext import commands

class Useful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description=f'Pong! API latency is: {round(self.client.latency * 1000)}ms'))

    @commands.group(name="help", aliases=['h', 'help?', '?'])
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            help_embed = discord.Embed(color=discord.Color.blue())
            help_embed.set_author(
                name="64 Stacks Police Bot",
                icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
            
            help_embed.add_field(name="Useful", value="``!help useful``", inline=True)
            help_embed.add_field(name="Server Management", value="``!help server``", inline=True)
            help_embed.add_field(name="User Management", value="``!help user``", inline=True)
            help_embed.add_field(name="Fun Commands", value="``!help fun``", inline=True)

            help_embed.set_footer(text="Need more help open a ticket under #support")

            await ctx.send(embed=help_embed)

    @commands.command()
    async def info(self, ctx):
        info_embed = discord.Embed(color=discord.Color.blue())
        info_embed.set_author(
            name="64 Stacks Police Bot",
            icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
        info_embed.add_field(name="**Server Info**", value=
            '**Server IP:** *Play.64Stacks.com*\n'
            '**Version:** *1.8-1.16*\n',
            inline=False)
        await ctx.send(embed=info_embed)

    @help.command(name='useful')
    async def help_useful(self, ctx):
        help_embed = discord.Embed(color=discord.Color.blue())
        help_embed.set_author(
            name="64 Stacks Police Bot",
            icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
        
        help_embed.add_field(name="**Commands**", value=
        '**!ping** *Simply states the bots current ping!*\n',
        inline=False)

        await ctx.send(embed=help_embed)
    
    @help.command(name='server')
    async def help_server(self, ctx):
        help_embed = discord.Embed(color=discord.Color.blue())
        help_embed.set_author(
            name="64 Stacks Police Bot",
            icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
        
        help_embed.add_field(name="**Commands**", value=
        '**!clear** **Amount** *Removes said amout of lines from the channel.*\n',
        inline=False)

        await ctx.send(embed=help_embed)
    
    @help.command(name='user')
    async def help_user(self, ctx):
        help_embed = discord.Embed(color=discord.Color.blue())
        help_embed.set_author(
            name="64 Stacks Police Bot",
            icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
        
        help_embed.add_field(name="**Commands**", value=
        '**!kick** **@mention** **Reason** *Kickes said user for said reason*\n'
        '**!ban** **@mention** **Reason** *Bans said user for said reason*\n'
        '**!unban** **username#1234** *Unbans said user.*\n',
        '**!ip** **IP Address/Domian Name** *Displays location data for an IP/Website.*\n',
        '**!whois** **@mention** *Displays useful user info.*\n',
        inline=False)

        await ctx.send(embed=help_embed)
    
    @help.command(name='fun')
    async def help_fun(self, ctx):
        help_embed = discord.Embed(color=discord.Color.blue())
        help_embed.set_author(
            name="64 Stacks Police Bot",
            icon_url="https://cdn.discordapp.com/avatars/738551372643041280/3c0b0df05f16ca7f426ca97aee40aba7.png")
        
        help_embed.add_field(name="**Commands**", value=
        '**!stealskin** *Show a users skin*\n'
        '**!colorcodes** *Shows Minecraft color codes.*\n',
        inline=False)

        await ctx.send(embed=help_embed)
    
def setup(client):
    client.add_cog(Useful(client))
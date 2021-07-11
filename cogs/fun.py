import aiohttp
import base64
import discord
import json
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ses = aiohttp.ClientSession()
    
    def cog_unload(self):
        self.client.loop.create_task(self.ses.close())
    
    @commands.command()
    async def colorcodes(self, ctx):
        embed = discord.Embed(color=discord.Color.blue(),
        description='Text in Minecraft can be formatted using different codes and\nthe section (``§``) sign.')

        embed.set_author(name="Minecraft Formatting Codes")
        
        embed.add_field(name="Color Codes", value=
        "<:red:746738331655602276> **Red** ``§c``\n"
        "<:yellow:746738331643150407> **Yellow** ``§e``\n"
        "<:green:746738331437760645> **Green** ``§a``\n"
        "<:aqua:746738331521384488> **Aqua** ``§b``\n"
        "<:blue:746738331521384468> **Blue** ``§9``\n"
        "<:light_purple:746738331555069972> **Light Purple** ``§d``\n"
        "<:white:746738331647475753> **White** ``§f``\n"
        "<:gray:746738331378778235> **Gray** ``§7``\n")

        embed.add_field(name="Color Codes", value=
        "<:dark_red:746738331525709934> **Dark Red** ``§4``\n"
        "<:gold:746738331190296668> **Gold** ``§6``\n"
        "<:dark_green:746738331198685216> **Dark Green** ``§2``\n"
        "<:dark_aqua:746738331580366849> **Dark Aqua** ``§3``\n"
        "<:dark_blue:746738331512995920> **Dark Blue** ``§1``\n"
        "<:dark_purple:746738331382972438> **Dark Purple** ``§5``\n"
        "<:dark_gray:746738331525578812> **Dark Gray** ``§8``\n"
        "<:black:746738331374583910> **Black** ``§0``\n")

        embed.add_field(name="Formatting Codes", value=
        "<:bold:746738331563327498> **Bold** ``§l``\n"
        "<:strikethrough:746738331613659226> ~~Strikethrough~~ ``§m``\n"
        "<:underline:746738331626242080> __Underline__ ``§n``\n"
        "<:italic:746738331395817514> *Italic* ``§o``\n"
        "<:obfuscated:746738331408269374> ||Obfuscated|| ``§k``\n"
        "<:reset:746738331378909255> Reset ``§r``\n")

        await ctx.send(embed=embed)
    
    @commands.command(name= "stealskin", aliases=["ss", "skin", "mcskin"])
    async def stealskin(self, ctx, *, gamertag: str):
        response = await self.ses.get(f"https://api.mojang.com/users/profiles/minecraft/{gamertag}")
        if response.status == 204:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description="That player doesn't exist."))
            return
        uuid = json.loads(await response.text()).get("id")
        if uuid is None:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description="That player doesn't exist."))
            return
        response = await self.ses.get(
            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}?unsigned=false")
        content = json.loads(await response.text())
        if "error" in content:
            if content["error"] == "TooManyRequestsException":
                await ctx.send(embed=discord.Embed(color=discord.Color.blue(), description="Slow down."))
                return
        if len(content["properties"]) == 0:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(),
                                               description="This user's skin can't be stolen for some reason..."))
            return
        undec = base64.b64decode(content["properties"][0]["value"])
        try:
            url = json.loads(undec)["textures"]["SKIN"]["url"]
        except Exception:
            await ctx.send(embed=discord.Embed(color=discord.Color.blue(),
                                               description="An error occurred while fetching that skin."))
            return
        skin_embed = discord.Embed(color=discord.Color.blue(),
                                   description=f"{gamertag}'s skin\n[**[Download]**]({url})")
        skin_embed.set_thumbnail(url=url)
        skin_embed.set_image(url=f"https://mc-heads.net/body/{gamertag}")
        await ctx.send(embed=skin_embed)

def setup(client):
    client.add_cog(Fun(client))
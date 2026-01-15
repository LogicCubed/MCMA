import os
import aiohttp
import discord
from discord.ext import commands

MC_API_KEY = os.getenv("MCMODELS_API_KEY")
BASE_URL = "https://api.mcmodels.net/v1/vendor"

class MCModelsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    async def list_products(self, ctx):
        headers = {
            "Authorization": f"Bearer {MC_API_KEY}",
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{BASE_URL}/products") as resp:
                if resp.status != 200:
                    return await ctx.send(f"❌ Failed to fetch products: {resp.status}")
                products_data = await resp.json()

        products = products_data.get("data", [])

        if not products:
            return await ctx.send("No products found.")

        embed = discord.Embed(
            title="Available Products 📦",
            color=0xF0075C
        )

        for p in products:
            name = p.get("name", "N/A")
            price = f"${p.get('base_price', 'N/A')}"
            embed.add_field(
                name=name,
                value=f"Price: {price}",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MCModelsCommands(bot))
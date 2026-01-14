import os
import aiohttp
from discord.ext import commands

MC_API_KEY = os.getenv("MCMODELS_API_KEY")
BASE_URL = "https://api.mcmodels.net/v1/vendor"

class MCModelsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="listproducts")
    async def list_products(self, ctx):
        headers = {"Authorization": f"Bearer {MC_API_KEY}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{BASE_URL}/products") as resp:
                if resp.status != 200:
                    return await ctx.send(f"❌ Failed to fetch products: {resp.status}")
                data = await resp.json()

        products = data.get("data", [])
        if not products:
            return await ctx.send("No products found.")

        msg_lines = [f"{p['id']}: {p['name']}" for p in products]
        msg = "\n".join(msg_lines)

        if len(msg) > 1900:
            msg = msg[:1900] + "\n…and more"

        await ctx.send(f"**Available Products:**\n{msg}")

async def setup(bot):
    await bot.add_cog(MCModelsCommands(bot))
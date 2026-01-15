import discord
from discord.ext import commands, tasks
import aiohttp
import os

MY_USER_ID = int(os.getenv("MY_USER_ID"))
API_KEY = os.getenv("MCMODELS_API_KEY")
BASE_URL = "https://api.mcmodels.net/v1/vendor"

class MCModelsPurchases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_purchase_id = None
        self.check_purchases.start()

    @tasks.loop(minutes=5)
    async def check_purchases(self):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"{BASE_URL}/purchases") as resp:
                if resp.status != 200:
                    return
                payload = await resp.json()


        purchases = payload.get("data", [])
        if not purchases:
            return

        latest = purchases[0]
        purchase_id = latest["id"]

        if self.last_purchase_id == purchase_id:
            return

        self.last_purchase_id = purchase_id

        package = latest["package"]
        product = latest["product"]

        embed = discord.Embed(
            title="💸 Purchase Alert 💸",
            color=0xF0075C
        )

        embed.add_field(name="Product 📦", value=package["name"], inline=False)
        embed.add_field(name="Total Sales 📈", value=str(latest["total"]), inline=True)
        embed.add_field(name="Revenue 💵", value=f"${product['received_amount']}", inline=True)

        user = await self.bot.fetch_user(MY_USER_ID)
        await user.send(embed=embed)

    @check_purchases.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MCModelsPurchases(bot))
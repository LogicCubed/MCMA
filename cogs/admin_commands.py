from discord.ext import commands
import discord
import os

MY_USER_ID = int(os.getenv("MY_USER_ID"))

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="setstatus", description="Set the bot's status (OWNER ONLY)")
    async def setstatus(self, interaction: discord.Interaction, status_text: str):
        if interaction.user.id != MY_USER_ID:
            return await interaction.response.send_message("❌ You are not allowed to use this command.", ephemeral=True)
        activity = discord.Game(name=status_text)
        await self.bot.change_presence(activity=activity)
        await interaction.response.send_message(f"✅ Bot status updated to: {status_text}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
from discord.ext import commands
import discord
import random

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Check if the bot is responsive")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("🏓 Pong!")

async def setup(bot):
    await bot.add_cog(UserCommands(bot))
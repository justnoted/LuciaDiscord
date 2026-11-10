import time

import discord
from discord import app_commands
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Check Lucia's latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer()

        start_time = time.time()
        await self.client.fetch_channel(interaction.channel_id)
        end_time = time.time()

        api_lat = round((end_time - start_time) * 1000)
        bot_lat = round(self.client.latency * 1000)

        embed = (discord.Embed(color=discord.Color(int(self.client.config['colors']['primary'], 16)))
                    .add_field(name="Latency", value=f"**API** - {api_lat} ms\n**Websocket** - {bot_lat} ms"))
        
        await interaction.followup.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Utility(client))
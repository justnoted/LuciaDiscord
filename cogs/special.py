import random

import discord
from discord import app_commands
from discord.ext import commands

from data.database import get_config_info


def create_choices_list(values_list):
    choices_list = []
    for value in values_list:
        choices_list.append(discord.app_commands.Choice(name=value, value=value))
    return choices_list


class Special(commands.Cog, description="<:Lucia:1253852411542372535>"):
    def __init__(self, client):
        self.client = client
        self.authorized_users = get_config_info("auth_users")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} is ready.")

    @app_commands.command(name="setactivity", description="Change Lucia's activity status")
    @app_commands.describe(activity_type="Set activity type", activity_description="Set an activity description", status="Set online, idle, or DND status", stream_url="Set streaming URL (only for Streaming activity)")
    @app_commands.choices(status=create_choices_list(["Online", "Idle", "DND"]), activity_type=create_choices_list(["Playing", "Streaming"]))
    async def set_activity(self, interaction: discord.Interaction, activity_description: str, activity_type: discord.app_commands.Choice[str] = None, status: discord.app_commands.Choice[str] = None, stream_url: str = None):
        if interaction.user.id not in self.authorized_users:
            embed = discord.Embed(description=f"**Invalid Permissions**. You aren't authorized to change activity status.", colour=discord.Color.yellow())
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)
            return

        check_status = status.value if status is not None else "Online"
        status_list = {"Online": discord.Status.online, "Idle": discord.Status.idle, "DND": discord.Status.dnd}
        check_activity = activity_type.value if activity_type is not None else "Playing"
        activity_list = {"Playing": discord.Game(name=activity_description),
                         "Streaming": discord.Streaming(name=activity_description, url=stream_url if stream_url else get_config_info("presence")["stream_url"])}

        await self.client.change_presence(status=status_list[check_status], activity=activity_list[check_activity])
        embed = discord.Embed(colour=discord.Color.green()).add_field(name="✔ Status Updated", value="Lucia's activity status has been changed.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shutdown", description="Shut down Lucia :3")
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id not in self.authorized_users:
            nope_responses = ["nope.", "not gonna happen, buddy", "absolutely not.", "ok fine, try again", "`approval = False`"]
            await interaction.response.send_message(content=random.choice(nope_responses))
            return

        await interaction.response.send_message(content="aye captain")
        await self.client.close()


async def setup(client):
    await client.add_cog(Special(client))
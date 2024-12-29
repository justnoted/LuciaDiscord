import discord
from discord.ext import commands
from discord import app_commands


def help_menu(interaction):
    lucia = interaction.client.get_user(1089292852963590224)
    embed = discord.Embed(colour=discord.Colour(0x3e038c))
    embed.set_author(name="Lucia", icon_url=lucia.avatar)
    return embed


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} is ready.")

    class HelpSelect(discord.ui.Select):
        def __init__(self, client):
            commands_list = {}
            options = []

            for cog in client.cogs.values():
                if cog.__cog_name__ == "Help":
                    continue

                options.append(discord.SelectOption(label=cog.__cog_name__, emoji=cog.description))
                commands_list[cog.__cog_name__] = ""
                for command in cog.walk_app_commands():
                    commands_list[cog.__cog_name__] += f"- `{command.name}` - {command.description}\n"

            self.commands_list = commands_list
            super().__init__(placeholder="Select a category", options=options)

        async def callback(self, interaction: discord.Interaction):
            category = self.values[0]
            embed = help_menu(interaction)
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            embed.add_field(name=category, value=self.commands_list[category], inline=False)
            await interaction.response.edit_message(embed=embed)

    class HelpMenu(discord.ui.View):
        def __init__(self, client):
            super().__init__(timeout=120)
            self.add_item(Help.HelpSelect(client=client))

    @app_commands.command(name="help", description="View Lucia's commands")
    async def help(self, interaction: discord.Interaction):
        embed = help_menu(interaction)
        noted = interaction.client.get_user(401134972360065028)
        embed.title = "Select an category below ✦"
        embed.description = "View Lucia's most recent changes on `/changelog` <:Lucia:1253852411542372535>"
        embed.set_footer(text=f"Developed by Noted :3", icon_url=noted.avatar)
        await interaction.response.send_message(embed=embed, view=self.HelpMenu(client=interaction.client))


async def setup(client):
    await client.add_cog(Help(client))
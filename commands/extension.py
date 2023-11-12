from enum import Enum
import discord
from valor import Valor
from discord import app_commands

async def extension(valor: Valor):
    group = app_commands.Group(name="extension", description="Commands for managing activated bot features")

    extensions_list = valor.all_extensions.copy()
    extensions_list.remove("commands.extension")
    Extensions = Enum("Extensions", extensions_list)

    @group.command(name="load", description="Load a bot feature")
    async def load(interaction: discord.Interaction, extension: Extensions):
        if extension.name in valor.extensions:
            await interaction.response.send_message(f"{extension.name} is already loaded")
            return
        await valor.load_extension(extension.name)
        await interaction.response.send_message(f"Loaded {extension.name}")

    @group.command(name="unload", description="Unload a bot feature")
    async def unload(interaction: discord.Interaction, extension: Extensions):
        if extension.name not in valor.extensions:
            await interaction.response.send_message(f"{extension.name} is already unloaded")
            return
        await valor.unload_extension(extension.name)
        await interaction.response.send_message(f"Unloaded {extension.name}")

    @group.command(name="reload", description="Reload a bot feature")
    async def reload(interaction: discord.Interaction, extension: Extensions):
        if extension.name not in valor.extensions:
            await valor.load_extension(extension.name)
            await interaction.response.send_message(f"Loaded {extension.name}")
            return
        await valor.reload_extension(extension.name)
        await interaction.response.send_message(f"Reloaded {extension.name}")

    @group.command(name="list", description="List all loaded bot features")
    @app_commands.describe(all="List all bot features, including unloaded ones")
    async def list(interaction: discord.Interaction, all: bool = False):
        extensions = ", ".join(valor.extensions)
        await interaction.response.send_message(f"Loaded extensions: {extensions}")

    valor.tree.add_command(group)

async def setup(valor: Valor):
    await extension(valor)
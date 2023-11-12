import discord
from valor import Valor
from discord import app_commands

async def test(valor: Valor):
    group = app_commands.Group(name="test", description="Test command")

    @group.command(name="test", description="Test command")
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message("Test")
    
    @group.command(name="test2", description="Test command 2")
    async def test2(interaction: discord.Interaction):
        await interaction.response.send_message("Test2")

    valor.tree.add_command(group)

async def setup(valor: Valor):
    await test(valor)
import logging

from core import Valor
from discord import Embed
from utils import AutoPagedEmbedView, PagedEmbedView

logger = logging.getLogger(__name__)


async def register_test_embed(valor: Valor):
    tree = valor.tree

    @tree.command(name="test-embed", description="Test PagedEmbedView")
    async def test_embed(interaction):
        embed1 = Embed(title="Page 1", description="This is the first page")
        embed1.add_field(name="Field 1", value="This is the first field")

        embed2 = Embed(title="Page 2", description="woah a second page")
        embed2.add_field(name="gaming", value="such gaming 2")

        embed3 = Embed(title="Page 3", description="woah a third page")
        embed3.add_field(name="gaming", value="such gaming 3")

        embeds = [embed1, embed2, embed3]

        view = PagedEmbedView(embeds)

        await interaction.response.send_message(embed=view.embeds[0], view=view)

    @tree.command(name="test-auto-embed", description="Test AutoPagedEmbedView")
    async def test_auto_embed(interaction, header: bool):
        content = "This is a test of the AutoPagedEmbedView\n" * 100
        view = AutoPagedEmbedView(content, header="This is a header" if header else None)

        await interaction.response.send_message(embed=view.embeds[0], view=view)


async def setup(valor: Valor):
    logger.info("Registering test_embed commands...")
    await register_test_embed(valor)

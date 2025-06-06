import discord
from discord.ui import View


class PagedEmbedView(View):
    def __init__(self, embeds: list[discord.Embed], attachments: list[discord.File | None] = [], timeout: int = 600):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.page = 0
        self.max_page = len(embeds) - 1
        self.attachments = attachments

    @discord.ui.button(emoji="⬅️", row=1, disabled=True)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        self.update_button_state()
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self, attachments=self.attachments)

    @discord.ui.button(emoji="➡️", row=1)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        self.update_button_state()
        await interaction.response.edit_message(embed=self.embeds[self.page], view=self, attachments=self.attachments)

    def update_button_state(self):
        if self.page == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False

        if self.page == self.max_page:
            self.children[1].disabled = True
        else:
            self.children[1].disabled = False


class AutoPagedEmbedView(PagedEmbedView):
    def __init__(self, content: str, header: str | None = None, timeout: int = 600):
        super().__init__([], timeout=timeout)
        self.content = content
        self.header = header
        self.page_embeds()

        self.max_page = len(self.embeds) - 1
        self.page = 0

    def page_embeds(self, limit: int = 1500):
        lines = self.content.split("\n")
        current_page = ""
        embeds = []

        limit = limit - len(self.header) + 1 if self.header else limit

        for line in lines:
            if len(current_page) + len(line) <= limit:
                current_page += line + "\n"
            else:
                page_content = self.header + "\n" + current_page.strip() if self.header else current_page.strip()
                embed = discord.Embed(description=page_content)
                embeds.append(embed)
                current_page = line + "\n"

        if current_page:
            page_content = self.header + "\n" + current_page.strip() if self.header else current_page.strip()
            embed = discord.Embed(description=page_content)
            embeds.append(embed)

        if len(embeds) > 1:
            for i, embed in enumerate(embeds):
                embed.set_footer(text=f"Page {i + 1}/{len(embeds)}")

        self.embeds = embeds

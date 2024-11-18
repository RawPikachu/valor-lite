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
    def __init__(self, content: str, timeout: int = 600):
        super().__init__([], timeout=timeout)
        self.content = content
        self.page_embeds()

    def page_embeds(self, limit: int = 1500):
        lines = self.content.split("\n")
        current_page = ""
        for line in lines:
            if len(current_page) + len(line) <= limit:
                current_page += line + "\n"
            else:
                self.embeds.append(discord.Embed(description=current_page))
                current_page = line + "\n"
        if current_page:
            self.embeds.append(discord.Embed(description=current_page))

        self.max_page = len(self.embeds) - 1

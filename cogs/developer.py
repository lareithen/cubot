import nextcord, config
from nextcord.ext import commands, application_checks

class developer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description='A developer command.', guild_ids=[config.GUILD])
    @application_checks.is_owner()
    async def test(self, interaction: nextcord.Interaction, option: str = nextcord.SlashOption(choices=['embed', 'message'])):
        if option == 'message':
            await interaction.send('Message')

        if option == 'embed':
            embed = nextcord.Embed(
                color=0,
                title='Title',
                description='Description'
            )
            embed.set_footer(text='Footer', icon_url=self.client.user.avatar)
            embed.add_field(name='Field Name', value='Field Value')
            embed.set_thumbnail(self.client.user.avatar)
            await interaction.send(embed=embed)

    @nextcord.slash_command(description='A developer command.', guild_ids=[config.GUILD])
    @application_checks.is_owner()
    async def print(self, interaction: nextcord.Interaction, arg: str = nextcord.SlashOption(required=True)):
        await interaction.send('Done.', ephemeral=True)
        await interaction.channel.send(arg)

def setup(client):
    client.add_cog(developer(client))
import nextcord, time, datetime
from nextcord.ext import commands

class general(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    @nextcord.slash_command(description='Displays informations about bot.')
    async def info(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title=f"About {self.client.user.name}", 
            color=0,
            description=f"**✨ Change Log**\n• Cubot v2.1 released."
        )

        current_time = time.time()
        difference = int(round(current_time - self.start_time))
        uptime = str(datetime.timedelta(seconds=difference))

        embed.add_field(name='Bot version', value='v2.1', inline=False)
        embed.add_field(name='Bot latency', value=f'{round(self.client.latency * 1000)} ms', inline=False)
        embed.add_field(name='Bot uptime', value=uptime, inline=False)
        embed.add_field(name='Bot library', value=f'nextcord=={nextcord.__version__}', inline=False)

        embed.set_footer(text='larei was here.')
        embed.set_thumbnail(url=self.client.user.avatar)
        await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(general(client))

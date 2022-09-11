import nextcord, config, time, datetime
from nextcord.ext import commands

class general(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.start_time = time.time()

    @nextcord.slash_command(description='Displays informations about bot.', guild_ids=[config.GUILD])
    async def info(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title=f"About {self.client.user.name}", 
            color=0,
            description=f"**✨ Change Log**\n• Cubot v2.0 released.\n• All commands changed to slash commands.\n• Added Watch Together feature.\n• Added snipe feature. :)"
        )

        current_time = time.time()
        difference = int(round(current_time - self.start_time))
        uptime = str(datetime.timedelta(seconds=difference))

        embed.add_field(name='Bot version', value='v2.0', inline=False)
        embed.add_field(name='Bot latency', value=f'{round(self.client.latency * 1000)} ms', inline=False)
        embed.add_field(name='Bot uptime', value=uptime, inline=False)
        embed.add_field(name='Bot library', value=f'nextcord=={nextcord.__version__}', inline=False)

        embed.set_footer(text='larei was here.')
        embed.set_thumbnail(url=self.client.user.avatar)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(description='Creates an invite for Watch Together.', guild_ids=[config.GUILD])
    async def youtube(self, interaction: nextcord.Interaction, channel: nextcord.VoiceChannel=nextcord.SlashOption(required=True)):
        try:
            invite_url = await channel.create_invite(target_application_id=880218394199220334, target_type=nextcord.InviteTarget.embedded_application)
        
            button = nextcord.ui.Button(label='Click me!', url=str(invite_url))
            view = nextcord.ui.View()
            view.add_item(button)
            embed = nextcord.Embed(
                color=16711680, # red
                title='Watch Together',
                description='Click the button below to join the party.'
            )
            await interaction.send(embed=embed, view=view)
        except:
            await interaction.send('An error occured.')

def setup(client):
    client.add_cog(general(client))

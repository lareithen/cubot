import nextcord, config, datetime
from nextcord.ext import commands

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if f'<@{self.client.user.id}>' == message.content:
                await message.channel.send(f'I am active.')

        if message.channel.id == config.SUGGESTIONS_CHANNEL:
            await message.add_reaction('⬆️')
            await message.add_reaction('⬇️')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.SERVER_STATUS_ROLE_MESSAGE:
            role = nextcord.utils.get(payload.member.guild.roles, id=config.SERVER_STATUS_ROLE)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == config.SERVER_STATUS_ROLE_MESSAGE:
            guild = self.client.get_guild(payload.guild_id)
            role = nextcord.utils.get(guild.roles, id=config.SERVER_STATUS_ROLE)
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

    """
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        message_time = message.created_at 
        now = datetime.datetime.now(datetime.timezone.utc)
        if now < message_time + datetime.timedelta(seconds=10):
            embed = nextcord.Embed(
                color=0,
                title=f'{message.author} said:',
                description=message.content
            )
            embed.set_footer(text='If you write a message and delete it within 10 seconds, Cubot will snipe it.', icon_url=self.client.user.avatar)
            await message.channel.send(embed=embed)
    """
        
def setup(client):
	client.add_cog(utils(client))
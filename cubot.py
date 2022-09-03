import nextcord, config, os, datetime
from nextcord.ext import commands, application_checks
from cooldowns import CallableOnCooldown #pip install function-cooldowns

intents=nextcord.Intents.default()
intents.message_content = True
client = commands.Bot(
    command_prefix=config.PREFIX, 
    help_command=None, 
    intents=intents,
    activity=nextcord.Game(name=config.ACTIVITY),
    status=nextcord.Status.idle
)

def noow():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time

@client.event
async def on_ready():
    member_count = client.get_guild(config.GUILD).member_count
    print(f"[{noow()}] - Bot logged in as '{client.user}', ready to serve to {member_count} users.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        ctx.send("Cubot now supports slash commands. Let's try to type /info.")

@client.event
async def on_application_command_error(interaction: nextcord.Interaction, error):
    error = getattr(error, 'original', error)
    
    if isinstance(error, CallableOnCooldown):
        await interaction.send(error)
    if isinstance(error, application_checks.errors.ApplicationMissingRole):
        await interaction.send('Missing required permission(s).')
    if isinstance(error, application_checks.errors.ApplicationNotOwner):
        await interaction.send('Missing required permission(s).')
    
print(f'[{noow()}] - The bot is starting...')
for file in os.listdir('cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f'[{noow()}] - cogs.{file[:-3]} loaded.')

client.run(config.TOKEN)

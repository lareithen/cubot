import nextcord, config, socket, cooldowns, socket, datetime
from nextcord.ext import commands, application_checks, tasks

class buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = False

    @nextcord.ui.button(label="Accept", style=nextcord.ButtonStyle.green)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.send('Process has been accepted, server will reboot in 5 seconds.', ephemeral=True)
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Decline", style=nextcord.ButtonStyle.red)
    async def decline(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.send('Process has been denied.', ephemeral=True)
        self.stop()

class server(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_server.start()

    @nextcord.slash_command(description='Reboots the game server.', guild_ids=[config.GUILD])
    @application_checks.has_role(config.SERVER_RESTARTER_ROLE)
    @cooldowns.cooldown(1, 60, bucket=cooldowns.SlashBucket.guild)
    async def reboot(self, interaction: nextcord.Interaction):
        btns = buttons()
        await interaction.send('The server will reboot, do you accept that?', view=btns, ephemeral=True)
        await btns.wait()
        if btns.value:
            try:
                os.system(f"taskkill /f /im \"{config.SERVER_FILE_NAME}\"")
                await asyncio.sleep(5)
                os.startfile(config.SERVER_FILE_PATH)
                await interaction.channel.send(f'**"Server is back online, have fun!"**\n~{interaction.user}')
            except Exception:
                await interaction.send('An error occurred.', ephemeral=True)
        else:
            return

    def check_port(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        return result

    def noow(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time

    @tasks.loop(seconds=5)
    async def check_server(self):
        check = self.check_port(config.SERVER_HOST, config.SERVER_PORT)
        channel = self.client.get_channel(config.SERVER_STATUS_CHANNEL)

        last_message = None
        try:
            last = (await channel.history(limit=1).flatten())[0].embeds[0].description
            last_message = last
        except:
            pass

        server_on_desc, server_off_desc = '🟢 The server is **UP** again, have fun!', '🔴 The server is currently **DOWN**, it will be back up as soon as possible!'
        server_on_embed = nextcord.Embed(
            title='Cubix Worlds Server Status',
            color=65280,
            description=server_on_desc
        )
        server_on_embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar)
        server_off_embed = nextcord.Embed(
            title='Cubix Worlds Server Status',
            color=16711680,
            description=server_off_desc
        )
        server_off_embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar)

        if check: # server off
            if last_message:
                if last_message == server_on_desc:
                    await channel.purge(limit=1)
                    await channel.send(embed=server_off_embed)
                    print(f'[{self.noow()}] - The server is off.')
            else:
                await channel.send(embed=server_off_embed)
                print(f'[{self.noow()}] - The server is off.')
        else: # server on
            if last_message:
                if last_message == server_off_desc:
                    await channel.purge(limit=1)
                    await channel.send(f'<@&{config.SERVER_STATUS_ROLE}>', embed=server_on_embed)
                    print(f'[{self.noow()}] - The server is on.')
            else:
                await channel.send(f'<@&{config.SERVER_STATUS_ROLE}>', embed=server_on_embed)
                print(f'[{self.noow()}] - The server is on.')
               
    @check_server.before_loop
    async def check_server_before(self):
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(server(client))

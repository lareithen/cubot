import nextcord, config
from nextcord.ext import commands, application_checks
from tinydb import Query, TinyDB

class winwin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.db = TinyDB('databases/winwin.json')
        self.query = Query()
        self.items = [
            {'tier': 1, 'amount': 20, 'name': 'Helper Role In-Discord'},
            {'tier': 2, 'amount': 40, 'name': '25 Cubix Coins'},
            {'tier': 3, 'amount': 75, 'name': 'Helper Badge In-Game'},
            {'tier': 4, 'amount': 100, 'name': 'Week of Free Premium Usership'},
            {'tier': 5, 'amount': 125, 'name': 'Special Helper T-Shirt In-Game'},
            {'tier': 6, 'amount': 150, 'name': 'Helper+ Role In-Discord + In-Game'},
            {'tier': 7, 'amount': 175, 'name': '60 Cubix Coins'},
            {'tier': 8, 'amount': 250, 'name': 'Supporter Role In-Discord + In-Game'},
            {'tier': 9, 'amount': 1000, 'name': '1 Special Prize'}
        ]

    def claim_list(self, tier):
        if tier == 0:
            return 'There are no rewards for now.'
        else:
            list_str = ''
            for i in range(tier):
                list_str += self.items[i]['name'] + '\n'
            return list_str

    @nextcord.slash_command(description='Creates account for you.', guild_ids=[config.GUILD])
    async def win_create_account(self, interaction: nextcord.Interaction):
        author = interaction.user
        author_db = self.db.get(self.query.id == author.id)
        if author_db:
            await interaction.send('You have already created an account.')
        else:
            self.db.insert({'id': author.id, 'points': 0, 'tier': 0})
            await interaction.send('Your account has been successfully created. ')

    @nextcord.slash_command(description="Displays the user's account.", guild_ids=[config.GUILD])
    async def win_account(self, interaction: nextcord.Interaction, user: nextcord.Member=nextcord.SlashOption(required=False)):
        embed = nextcord.Embed(color=0, title='')

        if user:
            user_db = self.db.get(self.query.id == user.id)
            if user_db:
                embed.title = f"{user}'s account"
                embed.add_field(name='Account ID', value=user_db['id'], inline=False)
                embed.add_field(name='Points', value=user_db['points'], inline=False)
                embed.add_field(name='Claim List', value=self.claim_list(user_db['tier']), inline=False)
                embed.set_thumbnail(url=user.avatar)
                await interaction.send(embed=embed)
            else:
                await interaction.send("This user doesn't have an account. Type /win_account to view your account.")
        else:
            author = interaction.user
            author_db = self.db.get(self.query.id == author.id)
            if author_db:
                embed.title = f"{author}'s account"
                embed.add_field(name='Account ID', value=author_db['id'], inline=False)
                embed.add_field(name='Points', value=author_db['points'], inline=False)
                embed.add_field(name='Claim List', value=self.claim_list(author_db['tier']), inline=False)
                embed.set_thumbnail(url=author.avatar)
                await interaction.send(embed=embed)
            else:
                await interaction.send("You don't have an account. If you want create it, use `/win_create_account` command.")

    @nextcord.slash_command(description='Sends specified amount of points to the specified user.', guild_ids=[config.GUILD])
    @application_checks.has_role(config.DEVELOPER_ROLE)
    async def win_give(self, interaction: nextcord.Interaction, user: nextcord.Member=nextcord.SlashOption(required=True), amount: int=nextcord.SlashOption(required=True)):
        user_db = self.db.get(self.query.id == user.id)
        if user_db:
            self.db.update({'points': user_db['points'] + amount}, self.query.id == user.id)
            await interaction.send(f'**{amount}** points successfully sent to **{user.name}**.')
        else:
            await interaction.send("This user doesn't have an account.")

    @nextcord.slash_command(description='Gives your claimable awards.', guild_ids=[config.GUILD])
    async def win_claim(self, interaction: nextcord.Interaction):
        author = interaction.user
        author_db = self.db.get(self.query.id == author.id)
        if author_db:
            tier = author_db['tier']
            points = author_db['points']
            bought = False
            await interaction.send('I am checking your account...')
            for item in self.items:
                if item['tier'] > tier:
                    if points >= item['amount']:
                        tier += 1
                        points -= item['amount']
                        self.db.update({'points': points}, self.query.id == author.id)
                        self.db.update({'tier': tier}, self.query.id == author.id)
                        bought = True
                        await interaction.send(f"**{item['name']}** added to claim list.")
                    if bought == False:
                        await interaction.send("You don't have enough points.")
                        break
                else:
                    continue
        else:
            await interaction.send(f"You don't have an account. If you want create it, use `/win_create_account` command.")

def setup(client):
    client.add_cog(winwin(client))

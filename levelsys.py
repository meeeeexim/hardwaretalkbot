import discord
from discord.ext import commands
from pymongo import MongoClient

bot_channel = 820629751290134568

talk_channels = [743080477128261665, 810418722665398302, 813372833354219550, 810418882094694430, 813738116354408488]

level = ["Tier D", "Tier C", "Tier B", "Tier A"]
levelnum = [5, 10, 20, 30]

cluster = MongoClient(
    "mongodb+srv://kakalouis:warrior#cats@hardwaretalk.vsgug.mongodb.net/hardwaretalk?retryWrites=true&w=majority")

levelling = cluster["hardwaretalk"]["leveling"]


class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 100}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl ** 2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1
                    xp -= ((50 * ((lvl-1) ** 2)) + (50 * (lvl - 1)))
                    if xp == 0:
                        await message.channel.send(f"Du bist nun Level {lvl}, {message.author.mention}. Weiter So!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level[i]))
                                levelRoleEm = discord.Embed(
                                    description=f"Herzlichen Glückwunsch {message.author.mention}, du hast die Rolle **{level[i]}** erhalten! Bleib weiterhin so aktiv!")
                                levelRoleEm.set_thumbnail(
                                    url="https://yt3.ggpht.com/ytc/AAUvwng7Vy2KJZGepepJdYoRBqKSyVlpUu6_RwgRFmDL=s176-c-k-c0x00ffffff-no-rj")
                                await levelschannel.send(embed=levelRoleEm)

    @commands.command()
    async def rank(self, ctx):
        if ctx.channel.id == bot_channel:
            stats = levelling.find_one({"id": ctx.author.id})
            if stats is None:
                noRank = discord.Embed(description="Du hast bisher noch keine Nachrichten verschickt!")
                await ctx.send(embed=noRank)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                    if xp < ((50 *(lvl ** 2)) + (50 * (lvl - 1))):
                        break
                    lvl += 1
                xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
                boxes = int((xp/(200 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                rankEmbed = discord.Embed(title="{}'s Level-Stats".format(ctx.author.name))
                rankEmbed.add_field(name="Nutzer:", value=ctx.author.mention, inline=True)
                rankEmbed.add_field(name="XP:", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
                rankEmbed.add_field(name="XP-Balken:", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
                rankEmbed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=rankEmbed)

    @commands.command()
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(title="XP-Leaderboard:")
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"XP: {tempxp}", inline=False)
                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)


#def setup(client):
#    client.add_cog(levelsys(client))

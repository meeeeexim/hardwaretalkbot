import aiofiles
import discord
from discord.ext import commands
import time
import asyncio
import praw
import os
import json
import random
import emoji
from discord.ext.commands import cooldown, BucketType
import levelsys
from discord_slash import SlashCommand, SlashContext

cogs = [levelsys]



mainshop = [{"name":"","price":400}]




reddit = praw.Reddit(client_id = "bpxQDDrhAmONCQ",
                    client_secret = "j2RkwTAYaYCHILzOsuPEUSQC_rZ2hA",
                    username = "m4ximr3dd1tz",
                    password = "warrior#cats",
                    user_agent = "prawlol")



intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix = "?", intents=intents)
slash = SlashCommand(client)


client.remove_command("help")

#for i in range(len(cogs)):
#    cogs[i].setup(client)

def leadingZero(time: str):
    if len(time) > 1:
        return time
    return "0" + time 


@client.group(invoke_without_command=True)
async def help(ctx):
    helpEm = discord.Embed(title = "Hilfe", description="Benutze ?help <command> um mehr Informationen über einen Command zu erhalten!", color=discord.Color.blue())

    helpEm.add_field(name="Meme-Commands", value = "meme, me_irl, cursedcomment")
    helpEm.add_field(name="Basic Economy-Commands", value="balance, deposit, withdraw")
    helpEm.add_field(name="Geld verdienen", value="beg, work")
    helpEm.add_field(name="Glücksspiel", value="slots, gamble, roulette")
    helpEm.add_field(name="Andere Economy-Commands", value="rob, send")

    await ctx.send(embed=helpEm)


@help.command()
async def meme(ctx):
    em = discord.Embed(title="Meme", description="Sendet ein zufälliges Meme aus dem r/Memes Subreddit.", color=discord.color.green())
    em.add_field(name="**Syntax**", value="?meme")


@slash.slash(name="slash")
async def slash(ctx: SlashContext):
    embed = discord.Embed(title="Dieser bot wird jetzt auch Slash-Commands unterstützen!", description="Slash-Commands - WOHOOO!", color=discord.Color.green())
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Hardwaretalk helfen'))
    print("Bot ist bereit!")


@client.event
async def on_member_join(member):

    welcome_message = random.choice([f"{member.mention} hat den Hardwaretalk-Server betreten!",
                                    f"Ein wildes {member.mention} ist auf dem Hardwaretalk-Discord erschienen!",
                                    f"{member.mention} ist der Hardwaretalk-Community beigetreten!",
                                    f"{member.mention} hat es geschafft den Weg zum Hardwaretalk-Discord zu finden!",
                                    f"{member.mention}, willkommen auf dem Hardwaretalk-Discord!"])


    welcomeEm = discord.Embed(title="Willkommmen!", description=welcome_message, color=discord.Color.blue())


    await client.get_channel(812243462492651561).send(embed=welcomeEm)


    em = discord.Embed(title="Willkommen!", description="Willkommen auf dem Hardwaretalk-Server! Akzeptiere die Regeln um dich zu verifizieren. Viel Spaß auf dem Server!", color=discord.Color.blue())
    em.set_thumbnail(url="https://yt3.ggpht.com/ytc/AAUvwng7Vy2KJZGepepJdYoRBqKSyVlpUu6_RwgRFmDL=s176-c-k-c0x00ffffff-no-rj")

    await member.send(embed=em)



@client.command(aliases=["bal"])
async def balance(ctx,*, member: discord.Member=None):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    if member != None:

        await open_account(member)

        member_wallet = users[str(member.id)]["wallet"]
        member_bank = users[str(member.id)]["bank"]
        mBalanceEm = discord.Embed(title = f"{member.name}'s Konto", color = discord.Color.red())
        mBalanceEm.add_field(name = "Geldbörse", value = str(member_wallet) + " HW-Dollar! \U0001F4B0")
        mBalanceEm.add_field(name = "Bankkonto", value = str(member_bank) + " HW-Dollar! \U0001F4B0")
        await ctx.send(embed= mBalanceEm)

    else:
        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        balanceEm = discord.Embed(title = f"{ctx.author.name}'s Konto", color = discord.Color.red())
        balanceEm.add_field(name = "Geldbörse", value = str(wallet_amt) + " HW-Dollar! \U0001F4B0")
        balanceEm.add_field(name = "Bankkonto", value = str(bank_amt) + " HW-Dollar! \U0001F4B0")
        await ctx.send(embed= balanceEm)

@balance.error
async def bal_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError.KeyError):
        em = discord.Embed(title="Fehler", description="Dieser Nutzer hat noch keinen Economy-Account!", color=discord.Color.red())
        await ctx.send(embed=em)
 
@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(250)

    randomWorkMsg = [f"Du baust deinem Freund einen PC zusammen und verdienst {earnings} \U0001F4B0",
                    f"Jemand kauft dir deinen Boxed Kühler für {earnings} \U0001F4B0",
                    f"Du gewinnst ein Fortnite Turnier und verdienst {earnings} \U0001F4B0",
                    f"Du machst GPU-Reselling und machst {earnings} \U0001F4B0 Profit.",
                    f"Dein PC wird geklaut und du erhältst {earnings} \U0001F4B0 Schadensersatz.",
                    f"Du gehst auf TikTok viral und bekommst {earnings} \U0001F4B0",
                    f"Du drehst 8-Jährigen Fake-VBucks an und bekommst {earnings} \U0001F4B0.",
                    f"Du gehst für {earnings} \U0001F4B0 Zeitungen austragen.",
                    f"Du malst ein hässliches Bild, was dir für {earnings} \U0001F4B0 abgekauft wird.",
                    f"Du findest {earnings} \U0001F4B0 auf der Straße.",
                    f"Du übertaktest deinen RAM auf 4000mhz und verkaufst ihn für {earnings} \U0001F4B0.",
                    f"Du scamst jemanden mit einem GPU-Bild für {earnings} \U0001F4B0.",
                    f"Du vertreibst 30 Kabelbinder für {earnings} \U0001F4B0.",
                    f"Dein Netzteil schmiert ab. Es wird dir von einem PC-Verkäufer für {earnings} \U0001F4B0 abgekauft.",
                    f"Du reparierst für {earnings} eine SSD, ohne zu wissen, was du tust.",
                    f"Du verkaufst geschmacklose Mauspads für {earnings} \U0001F4B0.",
                    f"Du erhältst {earnings} \U0001F4B0 wegen deinem Praktikum.",
                    f"Du verkaufst selektierte CPUs und bekommst {earnings} \U0001F4B0.",
                    f"Du installierst deiner Freundin für {earnings} \U0001F4B0 Grafiktreiber.",
                    f"Dein Freund kauft dir einen Wish-PC für {earnings} \U0001F4B0 ab.",
                    f"Du gewinnst ein Nitro-Giveaway und verkaufst deinen Account für {earnings} \U0001F4B0.",
                    f"Du verkaufst RGB-Headsets für {earnings} \U0001F4B0.",
                    f"Du klebst RGB-Stripes an deinen Stuhl und kriegst ihn mit {earnings} \U0001F4B0 Profit verkauft.",
                    f"Aus Mitleid kauft jemand deine hässlichen Mauspads für {earnings} \U0001F4B0.",
                    f"Du gibst Hardware-Nachhilfe und wirst nach einer Stunde mit {earnings} \U0001F4B0 rausgeschmissen.",
                    f"Du bemalst Cases und kannst {earnings} \U0001F4B0 verlangen.",
                    f"Jemand kauft dir ein H510 Custom-Frontpanel für {earnings} \U0001F4B0 ab.",
                    f"Deine Custom Sleeves werden für {earnings} \U0001F4B0 gekauft."]


    workEm = discord.Embed(title=f"{ctx.author.name}'s Job", description=random.choice(randomWorkMsg), color=discord.Color.green())
    await ctx.send(embed = workEm)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
         json.dump(users, f)

    wallet_amt = users[str(user.id)]["wallet"]


@work.error
async def work_error(ctx, error):
    cd = round(error.retry_after)
    minutes = str(cd // 60)
    seconds = str(cd % 60)        

    if minutes == "0":
        msg = f"Du musst noch {seconds}s warten!"
    else:
        msg = f'Du musst noch {leadingZero(minutes)}:{leadingZero(seconds)}m warten!'


    if isinstance(error, commands.CommandOnCooldown):
        
        embedWorkCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedWorkCooldown)



@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx):
     await open_account(ctx.author)

     users = await get_bank_data()

     user = ctx.author

     earnings = random.randrange(31)

     possibility = random.randint(0, 100)

     titles = ["Pepe sagt:",
                "Hardwaretalk sagt:",
                "Maxim das Developer sagt:",
                "Matthis sagt:",
                "Risitas sagt:",
                "Ich sage:"]


     if possibility>50:
        begEmbed = discord.Embed(title=random.choice(titles), description=f"Hier, {earnings} HW-Dollar für dich. Kauf dir ein Eis oder so.", color=discord.Color.green())
        await ctx.send(embed=begEmbed)
        
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        wallet_amt = users[str(user.id)]["wallet"]


     else:
         begNoEmbed = discord.Embed(title=random.choice(titles), description=f"Nö, jetzt nicht. Geh arbeiten oder so.", color=discord.Color.red())
         await ctx.send(embed=begNoEmbed)



@beg.error
async def beg_error(ctx, error):
    cd = round(error.retry_after)
    seconds = str(cd % 60)        

    msg = f'Du musst noch {seconds}s warten!'
    if isinstance(error, commands.CommandOnCooldown):
        embedBegCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedBegCooldown)


@client.command(aliases=["with"])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    amount = amount.strip().lower()

    if amount.isdigit():

        if amount == None:
            noWithAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du abheben willst!", color=discord.Color.red())
            await ctx.send(embed=noWithAmount)
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[1]:
            noWithMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht. Nicht gierig werden!", color=discord.Color.red())
            await ctx.send(embed=noWithMoney)
            return

        if amount<0:
            negativeAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben. Soll ich dir etwa Geld wegnehmen?", color=discord.Color.red())
            await ctx.send(embed=negativeAmount)
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1*amount, "bank")

        withdrawEm = discord.Embed(title="Abheben bestätigt! \u2705", description=f"Du hast {amount} HW-Dollar von deinem Konto abgehoben!", color=discord.Color.green())
        await ctx.send(embed=withdrawEm)

    if amount == "all":
        bal = await update_bank(ctx.author)

        amount = bal[1]

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1*amount, "bank")

        withdrawEm = discord.Embed(title="Abheben bestätigt! \u2705", description=f"Du hast {amount} HW-Dollar von deinem Konto abgehoben!", color=discord.Color.green())
        await ctx.send(embed=withdrawEm)        



@client.command(aliases=["dep"])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)


    amount = amount.strip().lower()

    if amount.isdigit():

        amount = int(amount)

        if amount == None:
            noDepAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du anlegen willst!", color=discord.Color.red())
            await ctx.send(embed=noDepAmount)
            return

        bal = await update_bank(ctx.author)

        if amount>bal[0]:
            noDepMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht in der Geldbörse. Nicht gierig werden!", color=discord.Color.red())
            await ctx.send(embed=noDepMoney)
            return

        if amount<0:
            negativeDepAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben.", color=discord.Color.red())
            await ctx.send(embed=negativeDepAmount)
            return


        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author, amount, "bank")

        depositEm = discord.Embed(title="Anlegen bestätigt! \u2705", description=f"Du hast {amount} HW-Dollar auf dein Konto gelegt!", color=discord.Color.green())
        await ctx.send(embed=depositEm)




    if amount == "all":

        bal = await update_bank(ctx.author)

        amount = bal[0]

        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author, amount, "bank")

        depositEm = discord.Embed(title="Anlegen bestätigt! \u2705", description=f"Du hast {amount} HW-Dollar auf dein Konto gelegt!", color=discord.Color.green())
        await ctx.send(embed=depositEm)



@client.command()
async def send(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)


    if amount == None:
        noSendAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du senden willst!", color=discord.Color.red())
        await ctx.send(embed=noSendAmount)
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        noSendMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht auf der Bank. Da muss wohl wer ohne dein Geschenk klarkommen...", color=discord.Color.red())
        await ctx.send(embed=noSendMoney)
        return

    if amount<0:
        negativeSendAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben. Wenn du etwas klauen willst, benutze ?rob.", color=discord.Color.red())
        await ctx.send(embed=negativeSendAmount)
        return


    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(member, amount, "bank")

    sendEm = discord.Embed(title="Geldtransfer bestätigt! \u2705", description=f"Du hast {amount} HW-Dollar an {member.name} überwiesen! ", color=discord.Color.green())
    await ctx.send(embed=sendEm)

@send.error
async def send_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError.KeyError):
        em = discord.Embed(title="Fehler", description="Dieser Nutzer hat noch keinen Economy-Account!", color=discord.Color.red())
        await ctx.send(embed=em)



@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def slots(ctx, amount):
        await open_account(ctx.author)

        if amount == None:
            noSlotsAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du setzen willst!", color=discord.Color.red())
            await ctx.send(embed=noSlotsAmount)
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[0]:
            noSlotsMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht in der Geldbörse. Den Automat kannst du nicht abziehen!", color=discord.Color.red())
            await ctx.send(embed=noSlotsMoney)
            return

        if amount<0:
            negativeSlotsAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben. So verlierst du dein Geld sogar noch schneller!", color=discord.Color.red())
            await ctx.send(embed=negativeSlotsAmount)
            return

        final = []
        for i in range(3):
            a = random.choice([":heart_eyes:", "\U0001F911", "\U0001F4B8"])

            final.append(a)

        await ctx.send(str(final))



        if final[0] == final[1] and final[0] == final[2] and final[1] == final[2]:
            if amount>50:
                await update_bank(ctx.author,3*amount)
                winSlotsJackpotEm = discord.Embed(title= "Herzlichen Glückwunsch! \U0001F973", description="Herzlichen Glückwunsch! Du hast den Jackpot geknackt und deinen Einsatz VERDREIFACHT! Eine Menge Geld hast du da!", color=discord.Color.green())
                await ctx.send(embed=winSlotsJackpotEm)
            else:
                await update_bank(ctx.author,2*amount)
                winSlotsEm = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description="Herzlichen Glückwunsch! Du hast zwar nicht den Jackpot geknackt, dein Einsatz verdoppelt sich aber trotzdem! Cool, was?", color=discord.Color.green())
                await ctx.send(embed=winSlotsEm)
        else:
            await update_bank(ctx.author, -1*amount)
            loseSlotsEm = discord.Embed(title="Schade...", description="Du hast leider verloren und damit deinen ganzen Einsatz verloren...Lass nicht den Kopf hängen, nächstes Mal klappt es bestimmt!", color=discord.Color.red())
            await ctx.send(embed=loseSlotsEm)

@slots.error
async def slots_error(ctx, error):
    msg = f'Du musst noch {error.retry_after}s warten!'
    if isinstance(error, commands.CommandOnCooldown):
        embedSlotsCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedSlotsCooldown)





@client.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)


    bal = await update_bank(member)

    if bal[0]<100:
        noRobMoney = discord.Embed(title = "Es ist es nicht wert mann...", description ="Es lohnt sich nicht, diesen Typen auszurauben, versuche es bei wem der mehr als 100 HW-Dollar hat!", color=discord.Color.red())
        await ctx.send(embed=noRobMoney)
        return

    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author,earnings)
    await update_bank(member, -1*earnings)

    if earnings>0:
        robEm = discord.Embed(title="Erfolgreicher Coup! \u2705", description=f"Du hast es geschafft, du hast {member.name} um ganze {earnings} HW-Dollar beraubt!", color=discord.Color.green())
        await ctx.send(embed=robEm)
    if earnings == 0:
        noRobEarnings = discord.Embed(title="Verdammt...", description="Verdammt, der Typ hier hat sein Geld gut versteckt...Du hast leider nichts verdient.", color=discord.Color.green())
        await ctx.send(embed=noRobEarnings)


@rob.error
async def rob_error(ctx, error):
   
    cd = round(error.retry_after)
    minutes = str(cd // 60)
    seconds = str(cd % 60)        

    msg = f'Du musst noch {leadingZero(minutes)}:{leadingZero(seconds)}m warten!'
    
    if isinstance(error, commands.CommandOnCooldown):
             
        embedRobCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedRobCooldown)

    if isinstance(error, commands.CommandInvokeError.KeyError):
        em = discord.Embed(title="Fehler", description="Dieser Nutzer hat noch keinen Economy-Account!", color=discord.Color.red())
        await ctx.send(embed=em)



@client.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def gamble(ctx, amount=None):
    await open_account(ctx.author)

    if amount == None:
        noSlotsAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du setzen willst!", color=discord.Color.red())
        await ctx.send(embed=noSlotsAmount)
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        noSlotsMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht in der Geldbörse. Den Automat kannst du nicht abziehen!", color=discord.Color.red())
        await ctx.send(embed=noSlotsMoney)
        return

    if amount<0:
        negativeSlotsAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben. So verlierst du dein Geld sogar noch schneller!", color=discord.Color.red())
        await ctx.send(embed=negativeSlotsAmount)
        return


    i = random.randint(0, 100)
    if i > 70:
        await update_bank(ctx.author,2*amount)
        winGambleEm = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description="Herzlichen Glückwunsch! Du hast gewonnen und deinen Einsatz verdoppelt!", color=discord.Color.green())
        await ctx.send(embed=winGambleEm)
    else:
        await update_bank(ctx.author, -1*amount)
        loseGambleEm = discord.Embed(title="Schade...", description="Du hast leider verloren und damit deinen ganzen Einsatz verloren...Lass nicht den Kopf hängen, nächstes Mal klappt es bestimmt!", color=discord.Color.red())
        await ctx.send(embed=loseGambleEm)

@gamble.error
async def gamble_error(ctx, error):
    cd = round(error.retry_after)
    minutes = str(cd // 60)
    seconds = str(cd % 60)        

    msg = f'Du musst noch {leadingZero(minutes)}:{leadingZero(seconds)}m warten!'

    if isinstance(error, commands.CommandOnCooldown):

        embedGambleCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedGambleCooldown)
    

@client.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def roulette(ctx, amount = None, bet=None):

    await open_account(ctx.author)

    if amount == None:
        noSlotsAmount = discord.Embed(title = "Fehler", description = "Du hast nicht angegeben, wie viel du setzen willst!", color=discord.Color.red())
        await ctx.send(embed=noSlotsAmount)
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        noSlotsMoney = discord.Embed(title = "Fehler", description = "So viel Geld hast du nicht in der Geldbörse. Den Automat kannst du nicht abziehen!", color=discord.Color.red())
        await ctx.send(embed=noSlotsMoney)
        return

    if amount<0:
        negativeSlotsAmount = discord.Embed(title="Fehler", description="Du hast einen negativen Betrag angegeben. So verlierst du dein Geld sogar noch schneller!", color=discord.Color.red())
        await ctx.send(embed=negativeSlotsAmount)
        return
    
    if bet == None:
        noBet = discord.Embed(title="Fehler", description="Du hast nicht angegeben, auf was du setzen willst! Deine Optionen sind: Gerade, Ungerade, Rot, Schwarz, Grün, [Individuelle Zahl von 1-36]!", color=discord.Color.red())
        await ctx.send(embed=noBet)
        return



    bet_number = random.randint(0, 36)
    odd = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
    even = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    green = [0]


    bet = bet.strip().lower()

    if bet.isdigit():
        if bet_number == bet:
            await update_bank(ctx.author, 3*amount)
            rouletteNumberWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die Zahl {bet_number} gezogen und deinen Einstaz verdreifacht!", color=discord.Color.green())
            await ctx.send(embed=rouletteNumberWin)
        elif int(bet) > 36:
            tooHighBet = discord.Embed(title="Fehler", description="Du hast mehr gesetzt als 36. Du darfst nur auf Zahlen von 1 bis 36 setzen.", color=discord.Color.red())
            await ctx.send(embed=tooHighBet)
            return
        elif int(bet) < 1:
            tooLowBet = discord.Embed(ttile="Fehler", description="Du hast weniger gesetzt als 1. Du darfst nur auf Zahlen von 1 bis 36 setzen.", color=discord.Color.red())
            await ctx.send(embed=tooLowBet)
        else:
            await update_bank(ctx.author, -1*amount)
            rouletteNumberLose = discord.Embed(title="Schade...", description=f"Du hast die Zahl {bet_number} gezogen. Du hast leider verloren und verlierst deinen gesamten Einsatz.", color=discord.Color.red())
            await ctx.send(embed=rouletteNumberLose)

    elif bet_number in red and bet == "rot":
        await update_bank(ctx.author, 2*amount)
        rouletteRedWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die Zahl {bet_number} gezogen. Sie gehört zu den roten Zahlen. Du hast deinen Einsatz verdoppelt!", color=discord.Color.green())
        await ctx.send(embed=rouletteRedWin)
    elif bet_number in black and bet == "schwarz":
        await update_bank(ctx.author, 2*amount)
        rouletteBlackWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die Zahl {bet_number} gezogen. Sie gehört zu den schwarzen Zahlen. Du hast deinen Einsatz verdoppelt!", color=discord.Color.green())
        await ctx.send(embed=rouletteBlackWin)
    elif bet_number in green and bet == "grün":
        await update_bank(ctx.author, 3*amount)
        rouletteGreenWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die 0 gezogen! Sie ist die einzige grüne Zahl. Du hast deinen Einsatz verdreifacht!", color=discord.Color.green())
        await ctx.send(embed=rouletteGreenWin)
    elif bet_number in even and bet == "gerade":
        await update_bank(ctx.author, 2*amount)
        rouletteEvenWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die Zahl {bet_number} gezogen. Diese Zahl ist gerade. Du hast deinen Einsatz verdoppelt!", color=discord.Color.green())
        await ctx.send(embed=rouletteEvenWin)
    elif bet_number in odd and bet == "ungerade":
        await update_bank(ctx.author, 2*amount)
        rouletteOddWin = discord.Embed(title="Herzlichen Glückwunsch! \U0001F973", description=f"Herzlichen Glückwunsch! Du hast die Zahl {bet_number} gezogen. Diese Zahl ist ungerade. Du hast deinen Einsatz verdoppelt!", color=discord.Color.green())
        await ctx.send(embed=rouletteOddWin)
    elif bet != "gerade" and bet != "ungerade" and bet != "grün" and bet != "schwarz" and bet != "rot":
        betInvalid = discord.Embed(title="Fehler", description=f"Du hast auf {bet} gesetzt. Das ist keine gültige Zahl oder Kategorie. Bitte wette auf Rot, Schwarz, Grün, Gerade, Ungerade oder eine Individuelle Zahl von 1 bis 36.", color=discord.Color.red())
        await ctx.send(embed=betInvalid)
    else:
        await update_bank(ctx.author, -1*amount)
        rouletteLose = discord.Embed(title="Schade...", description=f"Du hast die Zahl {bet_number} gezogen. Du hast leider verloren und verlierst deinen ganzen Einsatz.", color=discord.Color.red())
        await ctx.send(embed=rouletteLose)

@roulette.error
async def roulette_error(ctx, error):
    
    cd = round(error.retry_after)
    minutes = str(cd // 60)
    seconds = str(cd % 60)        

    msg = f'Du musst noch {leadingZero(minutes)}:{leadingZero(seconds)}m warten!'

    if isinstance(error, commands.CommandOnCooldown):
        
        embedRouletteCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedRouletteCooldown)


@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 5):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} der reichsten Leute auf dem Server!" , description = "Die Platzierung basiert auf dem Geld auf dem Bankkonto und in der Geldbörse!",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"Privatvermögen beträgt: {amt} HW-Dollar \U0001F4B0",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

@client.command()
@commands.has_any_role(743087718510362715, 812219811169697812, 743087537332944906)
async def addmoney(ctx, user: discord.Member, amount=None):
    if user == None:
        user = ctx.author

    await open_account(user)

    

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal





@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []

    top = subreddit.top(limit = 50)

    for submission in top:
        all_subs.append(submission)
    random_submission = random.choice(all_subs)

    name = random_submission.title
    url = random_submission.url

    memeEm = discord.Embed(title = name)

    memeEm.set_image(url = url)

    await ctx.send(embed=memeEm)
@meme.error
async def meme_error(ctx, error):
    msg = f'Du musst noch {error.retry_after: .2f}s warten!'
    if isinstance(error, commands.CommandOnCooldown):
        embedMemeCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedMemeCooldown)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cursedcomment(ctx):
    subreddit2 = reddit.subreddit("cursedcomments")
    all_subs2 = []

    top2 = subreddit2.top(limit = 50)

    for submission in top2:
        all_subs2.append(submission)
    random_submission2 = random.choice(all_subs2)

    name2 = random_submission2.title
    url2 = random_submission2.url

    cursedEm = discord.Embed(title = name2)

    cursedEm.set_image(url = url2)

    await ctx.send(embed=cursedEm)

@cursedcomment.error
async def cursed_error(ctx, error):
    msg = f'Du musst noch {error.retry_after: .2f}s warten!'
    if isinstance(error, commands.CommandOnCooldown):
        embedCursedCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedCursedCooldown)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def me_irl(ctx):
    subreddit3 = reddit.subreddit("me_irl")
    all_subs3 = []

    top3 = subreddit3.top(limit = 50)

    for submission in top3:
        all_subs3.append(submission)
    random_submission3 = random.choice(all_subs3)

    name3 = random_submission3.title
    url3 = random_submission3.url


    meIRLem = discord.Embed(title = name3)

    meIRLem.set_image(url= url3)

    await ctx.send(embed=meIRLem)

@me_irl.error
async def meirl_error(ctx, error):
    msg = f'Du musst noch {error.retry_after: .2f}s warten!'
    if isinstance(error, commands.CommandOnCooldown):
        embedMeIrlCooldown = discord.Embed(title="Halt, nicht so schnell!", description=msg, color=discord.Color.red())
        await ctx.send(embed=embedMeIrlCooldown)


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Bot wird ausgeschaltet!")
    await ctx.bot.logout()





client.run("Token")

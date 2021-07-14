from os import name
from re import A
import discord
import youtube_dl
from youtube_dl import YoutubeDL
import wikipedia
from webserver import keep_alive
import datetime
import asyncio
from PIL import Image
from io import BytesIO
import random
import aiohttp,asyncio
from discord import asset
from discord.ext import commands as client
from jproperties import Properties
from discord.ext import commands
import discord
from discord import user
from discord.ext import commands
import asyncio
from discord.flags import Intents
import discord
from discord import message
from discord import member
from discord.ext import    commands
from discord.utils import get
import random
import os
import asyncio
import json
from discord.member import flatten_user
from jproperties import Properties

configs = Properties()
with open('./secrets\config.properties', 'rb') as config_file:
    configs.load(config_file)

PREFIX = f'{configs.get("PREFIX").data}'
MUTE_REASON = f'{configs.get("MUTE_REASON").data}'
WELCOME = f'{configs.get("WELCOME_MSG_CHANNEL_NAME").data}'
BYE = f'{configs.get("GOODBYE_MSG_CHANNEL_NAME").data}'
BAN_REASON = f'{configs.get("BAN_REASON").data}'
WARN_REASON = f'{configs.get("WARN_REASON").data}'
KICK_REASON = f'{configs.get("KICK_REASON").data}'
MUTE_CHANNEL_ID = f'{configs.get("MUTE_CHANNEL_ID").data}'

custom_prefix = PREFIX

client = commands.Bot(command_prefix=PREFIX,intents=Intents.all())
client.remove_command("help")
client.credits = 'EEEEEEE'

rules = [":one: No Bad Words or you will get warned   ",

":two: no Spamming or you get muted for 3 minutes ",

":three: No girl talks. ",

":four: Keep chat active as much as you can ",

":five: Talk about different games and fight who the better player is "]

# def wiki_summary(arg):
#     defination = wikipedia.summary(arg, sentences=3, chars=1000)

# @client.event
# async def on_message(message):
#     words = message.content.split()
#     important_words = words[1:]

#     if message.content.startswith(f"{custom_prefix}define"):
#         words = message.content.split()
#         important_words = words[1:]
#         search = discord.Embed(title="Searching....", description=wiki_summary(important_words), color=discord.Color.blue())
        
#     await member.send(content=None, embed=search)



#     #all the music related stuff
is_playing = False

    # 2d array containing [song, channel]
music_queue = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

vc = "Genral ┇😉"

    #searching the item on youtube
def search_yt(item):
    with YoutubeDL( YDL_OPTIONS) as ydl:
        try: 
            info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
        except Exception: 
            return False

    return {'source': info['formats'][0]['url'], 'title': info['title']}

def play_next():
    if len(music_queue) > 0:
        is_playing = True

        #get the first url
        m_url = music_queue[0][0]['source']

        #remove the first element as you are currently playing it
        music_queue.pop(0)

        vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: play_next())
    else:
        is_playing = False

# infinite loop checking 
async def play_music():
    if len(music_queue) > 0:
        is_playing = True

        vc = ""

        m_url = music_queue[0][0]['source']
        
        #try to connect to voice channel if you are not already connected

        if vc == "" or not vc.is_connected() or vc == None:
            vc = await music_queue[0][1].connect()
        else:
            await vc.move_to(music_queue[0][1])
        
        print(music_queue)
        #remove the first element as you are currently playing it
        music_queue.pop(0)

        vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS), after=lambda e: play_next())
    else:
        is_playing = False

@client.command(name="play", help="Plays a selected song from youtube")
async def p(ctx, *args):
    query = " ".join(args)

    voice_channel = ctx.author.voice.channel

    # if ctx.voice_client == None:
    #     await ctx.voice_channel.connect()
    # else:
    #     await ctx.voice_client.move_to(voice_channel)


    if voice_channel is None:
    #you need to be connected so that the bot knows where to go
        await ctx.send("Connect to a voice channel!")
    else:
        song = search_yt(query)
        if type(song) == type(True):
            await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
        else:
            await ctx.send("Song added to the queue")
            music_queue.append([song, voice_channel])
            await ctx.voice_channel.connect()

            if is_playing == False:
                await play_music()

@client.command(name="queue", help="Displays the current songs in queue")
async def q(ctx):
    retval = ""
    for i in range(0, len(music_queue)):
        retval += music_queue[i][0]['title'] + "\n"

    print(retval)
    if retval != "":
        await ctx.send(retval)
    else:
        await ctx.send("No music in queue")

@client.command(name="skip", help="Skips the current song being played")
async def skip(ctx):
    if vc != "" and vc:
        vc.stop()
        #try to play next in the queue if it exists
        await play_music()

# @client.command()
# async def join(ctx):
#     if ctx.author.voice == None:
#         novcem = discord.Embed(title = "No voice!", description="You need to be in a voice channel to use this command", color=discord.Color.red())
#         await ctx.send(embed=novcem)

#     voice_channel = ctx.author.voice.channel

#     if ctx.voice_client == None:
#         await ctx.voice_channel.connect()
#     else:
#         await ctx.voice_client.move_to(voice_channel)

# @client.command()
# async def disconnect(ctx):
#     await ctx.voice_client.disconnect()


# @client.command()
# async def play(ctx, url):
#     ctx.voice_client.stop()
#     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_stream 1 -reconnect_deley_max 5', 'options': '-vn'}
#     YDL_OPTIONS = {'format':"bestaudio"}
#     vc = ctx.voice_client

#     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
#         info = ydl.extract_info(url, download=False)
#         url2 = info['format'][0]['url']
#         source = await discord.FFmpegOpusAudio.format_probe(url2, **FFMPEG_OPTIONS)
#         vc.play(source)

# @client.command()
# async def pause(ctx):
#     await ctx.voice_client.pause()
#     pauzeem = discord.Embed(title="Paused", description="The song has been paused :D ", color=discord.Color.red())
#     await ctx.send(embed=pauzeem)

# @client.command()
# async def resume(ctx):
#     await ctx.voice_client.resume()
#     resem = discord.Embed(title="Resumed", description="The song has been resumed :D ", color=discord.Color.green())
#     await ctx.send(embed=resem)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):  
        msg = 'Still on cooldown, please try again in {:.2f}s.'.format(
            error.retry_after) 
        em13 = discord.Embed(title="**Error Block**", 
                             color=discord.Color.red())
        em13.add_field(name="__Slowmode Error:__", value=msg) 
        await ctx.send(embed=em13)  
    if isinstance(error, commands.MissingRequiredArgument): 
        msg2 = "Please enter all the required arguments!" 
        em14 = discord.Embed(title="Error Block", color=discord.Color.red()) 
        em14.add_field(name="__Missing Required Arguments:__", value=msg2)
        await ctx.send(embed=em14) 
    if isinstance(error, commands.MissingPermissions): 
        msg3 = "You are missing permissions to use that command!"
        em15 = discord.Embed(title="**Error Block**",
                             color=discord.Color.red())
        em15.add_field(name="__Missing Permissions:__", value=msg3)
        await ctx.send(embed=em15)
    if isinstance(error, commands.CommandNotFound): 
        msg4 = "No command found!"
        em16 = discord.Embed(title="**Error Block**",
                             color=discord.Color.red())
        em16.add_field(name="__Command Not Found:__", value=msg4)
        await ctx.send(embed=em16)

TOKEN = f'{configs.get("TOKEN").data}'

# @client.command(aliases=['c','delete'])
# @commands.has_permissions(administrator = True)
# async def clear(ctx,amount=10):
#     await ctx.channel.purge(limit = amount)

@client.command()
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])

@client.command(aliases=['c','delete'])
@commands.has_permissions(administrator = True)
async def clear(ctx,amount=10):
    await ctx.channel.purge(limit = amount)

@client.command()
async def allrules(ctx):
    for each_rule in rules:
        await ctx.send(each_rule)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= KICK_REASON):
    em = discord.Embed(title = "Kick", description = reason,color = ctx.author.color)
    await member.send(embed =em)
    await ctx.send(f"{member.mention} has been kicked because {reason}")
    await ctx.guild.kick(discord.Object(id = member.id))

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= BAN_REASON):
    em = discord.Embed(title = "Ban", description = reason,color = ctx.author.color)
    await member.send(embed =em)
    await ctx.send(f"{member.mention} has been banned because {reason}")
    await ctx.guild.ban(discord.Object(id = member.id))


@client.command()
async def wanted( ctx, user: discord.Member=None):
    if user == None:
        user = ctx.author

    wanted = Image.open("wanted.jpg")

    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((177,177))

    wanted.paste(pfp, (120,212))

    wanted.save("profile.jpg")

    await ctx.send(file = discord.File("profile.jpg"))

@client.command()
@commands.has_permissions(ban_members=True)
async def unabn( ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):

            await ctx.guild.unban(discord.Object(id))
            await ctx.send(member_name +" has been unbanned!")
            return


        await ctx.send(member+" was not found")                    

@commands.Cog.listener()
async def on_member_join( ctx, member):
    channel=discord.utils.get(member.guild.channels, name=WELCOME)
    em = discord.Embed(title = "Welcome", value = f"""adade :smiley: OP :heart_eyes: :heart_eyes: :heart_eyes: {member.mention} just came here :pg_heart: Hi bro welcome to {member.guild.name} Don't forget to read #𝚁𝚄𝙻𝙴𝚂 :clipboard: Know about our server in #𝚂𝙴𝚁𝚅𝙴𝚁-𝚃𝙾𝚄𝚁 :airplane: :eyes: Your Registration Number - {member.count} ``-PG會Pororo父¥T``""")

    await ctx.send(embed = em)

@commands.Cog.listener()
async def on_member_remove( ctx, member):
    channel=discord.utils.get(member.guild.channels, name=BYE)
    em = discord.Embed(title = "Bye", value = f"""ahhhhh... :cry: {member.id} just left the server:pensive:
    I hope you to come back:slight_frown:
    Until then, we'll wait for you:v:
    Galaxy Gaming Tamil aka Pororo""")

    await ctx.send(embed = em)

@client.command(aliases=['w'])
@commands.has_permissions(kick_members = True)
async def warn(ctx,member : discord.Member,*, reason = WARN_REASON):
    em = discord.Embed(title = "Warn", description = reason,color = ctx.author.color)
    await member.send(embed = em)
    await ctx.send(member.mention+ f" has been warned because {reason}")

# @client.command(aliases=['m'])
# @commands.has_permissions(kick_members=True)
# async def mute( ctx,member : discord.Member,*,reason = MUTE_REASON):
#     muted_role = ctx.guild.get_role(864763439968682005)
#     em = discord.Embed(title = "Mute", description = reason,color = ctx.author.color)

#     await member.add_roles(muted_role)

#     await ctx.send(f"{member.mention} has been muted because {reason}")
#     await member.send(embed = em)


@client.command()
@commands.has_role("Giveaways")
async def gstart(ctx, mins : int, * , prize: str):
    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60) 

    embed.add_field(name = "Ends At:", value = f"{end} UTC")
    embed.set_footer(text = f"Ends {mins} mintues from now!")

    my_msg = await ctx.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(mins*60)


    new_msg = await ctx.channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]
@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?", 
                "What should be the duration of the giveaway? (s | m | h | d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return            

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


    new_msg = await channel.fetch_message(my_msg.id)


    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command()
@commands.has_permissions(administrator = True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!")



@client.command(aliases=['tempmute'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member=None, time=None, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    if not member:
        await ctx.send("You must mention a member to mute!")
    elif not time:
        await ctx.send("You must mention a time!")
    else:
        if not reason:
            reason="No reason given"
        #Now timed mute manipulation
        try:
            seconds = time[:-1] #Gets the numbers from the time argument, start to -1
            duration = time[-1] #Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return
        guild = ctx.guild
        Muted = discord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}")
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(seconds)
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Mute over!", description=f"{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}")
        await ctx.send(embed=unmute_embed)





@client.command()
async def invite( ctx):
    em = discord.Embed(
        totle="Invite me from here-",
        description=f"https://discord.com/api/oauth2/authorize?client_id=864763081342058526&permissions=8&scope=bot",
        color=ctx.author.color,
    )
    await ctx.send(embed=em)

@client.command(aliases=['um'])
async def unmute( ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(864763439968682005)
    em = discord.Embed(title = "Un-Mute", description = "You have been un-muted",color = ctx.author.color)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention + " has been un-muted")
    await member.send(embed = em)

@client.command(aliases=['info'])
async def whois( ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention , color = discord.Colour.green())
    embed.add_field(name = "ID", value = member.id , inline = True )
    embed.add_field(name = "All-Roles", value = [role.mention if role.name != "@everyone" else role.name for role in member.roles] , inline = True )
    embed.add_field(name = "Top-Role", value = member.top_role.mention , inline = True )
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(aliases=["bal"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def balance(ctx, member: discord.Member = None):
    user = user = member if member else ctx.author
    await open_account(user)
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em2 = discord.Embed(
        title=f"__{user.name}'s Balance__",
        color=discord.Color.green(),
        timestamp=ctx.message.created_at,
    )
    em2.add_field(name="Wallet:",
                  value=f":coin:{wallet_amt}",
                  inline=False)
    em2.add_field(name="Bank:",
                  value=f":coin:{bank_amt}",
                  inline=False)
    em2.set_footer(text="⏰")
    await ctx.send(embed=em2)


beg_and_work_list = [
    "__PewDiePie__",
    "__MrBeast__ ",
    "__Dream__ ",
    "__Discord™__ ",
    "__Lil ツ#6699__",
    "__MustafaXD#9999__",
    "__Sengolda#1111__"
]



@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(400)

    beg_em = discord.Embed(title=f"{random.choice(beg_and_work_list)}",
                           color=discord.Color.green())
    beg_em.add_field(name=f"+ :coin:{earnings}",
                     value="Nice Begging!")
    await ctx.send(embed=beg_em)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 2000
        users[str(user.id)]["bank"] = 2000

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
        return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(10000, 30000)

    bege_em = discord.Embed(title=f"{random.choice(beg_and_work_list)}",
                           color=discord.Color.green())
    bege_em.add_field(name=f"+ :coin:{earnings}",
                     value="Daily Claimed!")
    await ctx.send(embed=bege_em)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 2000
        users[str(user.id)]["bank"] = 2000

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
        return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

@client.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    earnings = random.randrange(2500, 9000)

    work_em = discord.Embed(title=f"{random.choice(beg_and_work_list)}",
                           color=discord.Color.green())
    work_em.add_field(name=f"+ :coin:{earnings}",
                     value="Nice Keep working hard!")
    await ctx.send(embed=work_em)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 2000
        users[str(user.id)]["bank"] = 2000

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
        return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

mainshop = [{
    "name": "Watch",
    "price": 100,
    "description": "Time"
}, {
    "name": "Laptop",
    "price": 1000,
    "description": "Work"
}, {
    "name": "Gaming PC",
    "price": 10000,
    "description": "Gaming"
}, {
    "name": "Phone",
    "price": 4000,
    "description": "Call"
}, {
    "name": "Pistol",
    "price": 20000,
    "description": "Security"
}]


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def shop(ctx):
    em = discord.Embed(title="__Shop__ :shopping_cart:",
                       color=discord.Color.green())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name,
                     value=f":coin:{price} | {desc}")

    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(
                f"You don't have enough money in your wallet to buy :coin:{amount} {item}!"
            )
            return

    await ctx.send(f"You just bought {amount} {item}!")




@client.command(aliases=["inv"])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
      inventory = users[str(user.id)]["inventory"]

    except KeyError:
      return await ctx.send("error_msg")
      
    
    em_inv = discord.Embed(title="__Inventory__", color = discord.Color.green())
    for item in inventory:
      name = item["item"]
      amount = item["amount"]

      if not amount == 0:
        em_inv.add_field(name=name, value=amount, inline=False)

      
  
    await ctx.send(embed=em_inv)

    


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["inventory"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["inventory"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["inventory"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


@client.command(aliases=["with"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have enough money!")
        return

    if amount < 0:
        await ctx.send("Amount must be positive!")

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")
    await ctx.send(
        f"{ctx.author.mention} | You withrew :coin:{amount}!"
    )


@client.command(aliases=['dep'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def deposit(ctx, amount=None):
    try:
        await open_account(ctx.author)
        if amount == None:
            embed = discord.Embed(title="You can't withdraw nothing<:huh_evo:715500258305507388>", colour = discord.Colour.random())
            embed.set_footer(text="today")
            await ctx.reply(embed=embed)
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            user = ctx.author
            users = await get_bank_data()
            wallet_amt = users[str(user.id)]["wallet"]
            
            users[str(user.id)]["bank"] += wallet_amt
            users[str(user.id)]["wallet"] -= wallet_amt
            with open('bank.json' , 'w+') as f:
                json.dump(users,f)
                embed = discord.Embed(title=f"You deposited {wallet_amt} coins💰", colour = discord.Colour.random())
                embed.set_footer(text="today")
                await ctx.reply(embed=embed)
                return

        elif int(amount) > bal[0]:
            embed = discord.Embed(
                title="You don't have that much money in the wallet<:huh_evo:715500258305507388>", colour = discord.Colour.random())
            embed.set_footer(text="today")
            await ctx.reply(embed=embed)
            return
        elif int(amount) < 0:
            embed = discord.Embed(
                title="You can't deposit negitive amounts<:huh_evo:715500258305507388>", colour = discord.Colour.random())
            embed.set_footer(text="today")
            await ctx.reply(embed=embed)
            return
        
        else:
            await update_bank(ctx.author, int(amount), "bank")
            await update_bank(ctx.author, -1*int(amount))
            embed = discord.Embed(title=f"You deposited {amount} coins💰", colour = discord.Colour.random())
            embed.set_footer(text="today")
            await ctx.reply(embed=embed)
    except ValueError:
        await ctx.send("This isn't a valid argument")


@client.command(name="share", aliases=['give'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def share(ctx, member: discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the amount!")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have enough money!")
        return

    if amount < 0:
        await ctx.send("Amount must be positive!")

    await update_bank(ctx.author, -1 * amount, "bank")
    await update_bank(member,round(amount - (amount * 0.05)), "bank")

    await ctx.send(
        f"{ctx.author.mention} | You gave :coin: {round((amount - amount * 0.05))} to {member.name} | 5% Tax Rate"
    )


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal

@client.command(aliases=['Sell, SELL'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have {amount} {item} in your inventory."
                           )
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your inventory.")
            return

    await ctx.send(
        f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["inventory"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]

# Emailing System
@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def email(ctx, dmmem: discord.Member, *, thing):
    author = ctx.author
    if dmmem == ctx.author:
        await ctx.send(
            f"{author.mention} You can not send an email to yourself!")

    else:
        em5 = discord.Embed(
            title=":mailbox: Email",
            description=thing,
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        )
        em5.add_field(name="By:", value=ctx.author)
        em5.set_footer(text="⏰")
        await dmmem.send(embed=em5)
        await ctx.send(f"Email Send to {dmmem}!")

@client.command(aliases=["r"])
@commands.cooldown(1, 300, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)

    if bal[0] < 1000:
        embed = discord.Embed(
            title="Not Worth It",
            discription="Not worht it man, its not worth robbing him",
            color=ctx.author.color,
        )

    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author, earnings)
    await update_bank(member, -1 * earnings)

    embed = discord.Embed(
        title="Congratulations!",
        description=f"Congratulations! you robbed {earnings} coins",
        color=ctx.author.color,
    )

    await ctx.send(embed=embed)

client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter a valid amount! ")

    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal [0]

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("You don't have enough money in your bank!")
        return

    final = []
    for i in range(3):
        a = random.choice(["X","Q","Y"])

        final.append(a)

    await ctx.send(final)

    if final[0] == final [1] and final [0] == final [2] and final [1] == final [2]:
        await update_bank(ctx.author, 5 * amount, "wallet")
        await ctx.send(f"You won {amount*5}")

    elif final[0] == final [1] or final [0] == final [2] or final [1] == final [2]:
        await update_bank(ctx.author, 2 * amount, "wallet")
        await ctx.send(f"You won {amount*2}")

    else:
        await update_bank(ctx.author, -1 * amount, "wallet")
        await ctx.send(f"You lost {amount}")

@client.command(aliases=["lb", "rich"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(
        title=f"Top {x} Richest People",
        description="This is decided on the basis of raw money in the bank and wallet",
        color=ctx.author.color,
    )
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


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


async def update_bank( user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal

_8ball_res = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]


@client.command(aliases=['am'], help="Adds money to a user")
@commands.has_permissions(kick_members=True)
async def addmoney(ctx, amount=None, user: discord.Member = None):
    if user == None:
        user = ctx.author
    elif amount == None:
        await ctx.reply("Enter the amount of money to be added")
        return
    await open_account(user)
    amount = int(amount)
    users = await get_bank_data()
    users[str(user.id)]["wallet"] += amount
    embed = discord.Embed(
        title=f"Money💰 given to {user}👨‍🎨 by {ctx.author}👨‍🎨", colour=discord.Color.magenta())
    embed.add_field(
        name=f"Successfully Transferred `{amount}` to `{user}`", value=f"{user} be poor lol")
    await ctx.reply(embed=embed)
    with open('bank.json', 'w') as f:
        json.dump(users, f)

@client.command(aliases=['rm'], help="Removes money to a user")
@commands.has_permissions(kick_members=True)
async def removemoney(ctx, amount=None, user: discord.Member = None):
    if user == None:
        user = ctx.author
    elif amount == None:
        await ctx.reply("Enter the amount of money to be Removed")
        return
    await open_account(user)
    amount = int(amount)
    users = await get_bank_data()
    users[str(user.id)]["wallet"] -= amount
    embed = discord.Embed(
        title=f"Money💰 taken from {user}👨‍🎨 by {ctx.author}👨‍🎨", colour=discord.Color.magenta())
    embed.add_field(name=f"Successfully Removed `{amount}` from `{user}`", value=f"{user} be rich omg")
    await ctx.reply(embed=embed)
    with open('bank.json', 'w') as f:
        json.dump(users, f)

@client.command()
async def meme( ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r/memes/top.json") as response:
                j = await response.json()
                data = j["data"]["children"][random.randint(0, 25)]["data"]
                image_url = data["url"]
                title = data["title"]
                em = discord.Embed(description=f"[**{title}**]({image_url})", color=ctx.author.color)
                em.set_image(url=image_url)
                em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
                await ctx.send(embed=em)
    except:
        pass
@client.command(name='8ball')
async def _8ball( ctx):
    await ctx.send(random.choice(_8ball_res))

@client.command()
async def party( ctx,*,reason: commands.clean_content = None):
    reason = ""+reason if reason else "Unknown reason"
    msg = '''\nHosted by: {0.name}\nReason:{1}'''.format(ctx.author,reason)
    em = discord.Embed(title="Party!!", description=msg, color=ctx.author.color)
    msg = await ctx.send(embed = em)
    await msg.add_reaction("🎉")
    await asyncio.sleep(10)

    users = (
        await(await ctx.channel.fetch_message(int(msg.id)))
        .reactions[0]
        .users()
        .flatten()
    )

    return_data = ", \u200b".join(
        [
            discord.utils.escape_mentions(i.display_name)
            for i in users
            if not i.bot
        ]
    )
    await ctx.send('{0} Enjoy the party!'.format(return_data))

@client.command()
async def ping( ctx):
        em=discord.Embed(
            title="Pong",
            description="",
            color=discord.Color.blue()
        )
        await ctx.send(embed=em)


@client.group(invoke_without_command=True)
async def help(ctx):
    # em = discord.Embed(title = "Help", description = "help cmd",color = ctx.author.color)
    em = discord.Embed(title = "Help", description = f"Use ``{custom_prefix}help <command>`` / ``{custom_prefix}help <category>`` for extended information on a command.",color = ctx.author.color)

    em.add_field(name = "**Moderation**", value= f"use ``{custom_prefix}help mod`` for extended information on this command", inline = True)
    em.add_field(name = "**Fun**", value= f"use ``{custom_prefix}help fun`` for extended information on this command", inline = True) 
    em.add_field(name = "**Economy**", value= f"use ``{custom_prefix}help economy`` for extended information on this command", inline = True) 
    print("Print values have started")
    await ctx.send(embed = em)

@help.command()
async def mod(ctx):
    
    em = discord.Embed(title = "Moderation", description = "``kick | ban | mute | unban | unmute | warn | clear chat | rule | allrules``", color = ctx.author.color)

    await ctx.send(embed=em)

@help.command()
async def fun(ctx):

    em = discord.Embed(title = "Fun", description = "``8Ball | meme | party | ping | whois | emoji``", color = ctx.author.color)
    # em.add_field(name="Fun", decription="")

    await ctx.send(embed=em)

@help.command()
async def economy(ctx):

    em = discord.Embed(title = "Economy", description = "```beg | work | rob | slots | balance | bag | shop | buy | sell | deposit | withdraw | leaderboard | send```", color = ctx.author.color)

    await ctx.send(embed=em)

@help.command(aliases=["nocategory"])
async def no_category(ctx):

    em = discord.Embed(title = "No Category", description = "help", color = ctx.author.color)
    # em.add_field(name = "", description="help")

    await ctx.send(embed=em)



@help.command(name="8ball")
async def _8ball(ctx):

    em = discord.Embed(
        title="8Ball",
        description="8BALL",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}8ball``")

    await ctx.send(embed=em)

@help.command()
async def meme(ctx):

    em = discord.Embed(
        title="Meme",
        description="Sends a meme",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}meme```")

    await ctx.send(embed=em)

@help.command()
async def party(ctx):

    em = discord.Embed(
        title="Party",
        description="Starts a party!!",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}party```")

    await ctx.send(embed=em)

@help.command()
async def ping(ctx):

    em = discord.Embed(
        title="Ping",
        description="Sends back 'pong' ",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}ping```")

    await ctx.send(embed=em)


@help.command()
async def beg(ctx):

    em = discord.Embed(
        title="Beg",
        description="gives you free money every 20 seconds",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}beg```")

    await ctx.send(embed=em)


@help.command()
async def rob(ctx):

    em = discord.Embed(
        title="Rob",
        description="Lets you rob a person and get their money",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}rob <member>```")

    await ctx.send(embed=em)


@help.command()
async def slots(ctx):

    em = discord.Embed(
        title="Slots",
        description="It's a gamble. Gamble your money and have a 1 in 3 chance of wining",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}slots [amt]```")

    await ctx.send(embed=em)


@help.command()
async def balance(ctx):

    em = discord.Embed(
        title="Balance",
        description="Lets you see your bank and wallet status",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}balance``` | ```!b```")

    await ctx.send(embed=em)

@help.command()
async def wanted(ctx):
    em = discord.Embed(
        title="Wanted",
        description="Shows a users pfp opn a wanted poster",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"``{custom_prefix}wanted <user>``")

    await ctx.send(embed=em)

@help.command()
async def bag(ctx):

    em = discord.Embed(
        title="Bag",
        description="Shows you all the items you have bought",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}bag```")

    await ctx.send(embed=em)


@help.command()
async def shop(ctx):

    em = discord.Embed(
        title="Shop",
        description="Shows you all the items available in the shop that you can buy",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}shop```")

    await ctx.send(embed=em)


@help.command()
async def buy(ctx):

    em = discord.Embed(
        title="Buy",
        description="Lets you buy items from the shop",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}buy <item>```")

    await ctx.send(embed=em)


@help.command()
async def sell(ctx):

    em = discord.Embed(
        title="Sell",
        description="Lets you sell items in your bag",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}sell [amt] <item>``` | ```{custom_prefix}sell <item>```")

    await ctx.send(embed=em)


@help.command()
async def deposit(ctx):

    em = discord.Embed(
        title="Deposit",
        description="Lets you deposit money in your bank to keep it safe from people stealing it",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}deposit [amt]``` | ```!dep [amt]```")

    await ctx.send(embed=em)


@help.command()
async def withdraw(ctx):

    em = discord.Embed(
        title="Withdraw",
        description="Lets you withdraw items from your bank so that you can buy items",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}with [amt]``` | ```!withdraw [amt]```")

    await ctx.send(embed=em)


@help.command()
async def leaderboard(ctx):

    em = discord.Embed(
        title="Leaderboard",
        description="Shows the current leaderboard for the top 3 members",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}leaderboard```")

    await ctx.send(embed=em)


@help.command()
async def send(ctx):

    em = discord.Embed(
        title="Send",
        description="Lest you send money to yor friends from your bank",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}send <member> [amt]```")

    await ctx.send(embed=em)

@help.command()
async def work(ctx):

    em = discord.Embed(
        title="Work",
        description="Lets you earn money every 2 minutes",
        color=ctx.author.color,
    )

    em.add_field(name="**Syntax**", value=f"```{custom_prefix}work```")

    await ctx.send(embed=em)


@help.command()
async def kick(ctx):

    em = discord.Embed(title = "Kick", description = "Kicks a member from the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}kick <member> [reason]")


    await ctx.send(embed = em)


@help.command()
async def ban(ctx):

    em = discord.Embed(title = "**Ban**", description = "Bans a member from the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}ban <member> [reason]")

    await ctx.send(embed = em)

@help.command()
async def mute(ctx):

    em = discord.Embed(title = "Mute", description = "Mutes a member in the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}mute <member>")


    await ctx.send(embed = em)

@help.command()
async def unban(ctx):

    em = discord.Embed(title = "Un-Ban", description = "Un-Bans a member from the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}unban <member>")

    await ctx.send(embed = em)

@help.command()
async def unmute(ctx):

    em = discord.Embed(title = "Un-Mute", description = "Un-Mutes a member in the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}unmute <member>")

    await ctx.send(embed = em)

@help.command()
async def whois(ctx):

    em = discord.Embed(title = "Who-Is", description = "Gives the genral information of a member",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}whois <member>")


    await ctx.send(embed = em)

@help.command()
async def Warn(ctx):

    em = discord.Embed(title = "Warn", description = "Kicks a member from the server",color = ctx.author.color)

    em.add_field(name  = "**Syntax**", value = f"{custom_prefix}kick <member> [reason]")

    await ctx.send(embed = em)

keep_alive()

def bot_starter():
    print("Services Have Started")
    client.run("ODY0NzYzMDgxMzQyMDU4NTI2.YO6LYQ.TFTt9EG7sgC9oYoFQrDxMKN8-A8")

bot_starter()
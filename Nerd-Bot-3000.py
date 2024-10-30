# Import API's + other stuff
import discord, asyncio
from datetime import datetime, timedelta
from discord.ext import commands

# Set Bot intents, Create Bot object
intents = discord.Intents.default()
intents.members = True
Bot = commands.Bot(command_prefix='!', intents=intents)
global MemberRole1, MemberRole2, FriendRole, TimeOutMember, EndTime
EndTime = datetime.now()

# Prints to Console when connected
@Bot.event
async def on_ready():

    # Gets Guild, target User/Roles
    global MemberRole1, MemberRole2, FriendRole, TimeOutMember
    ServerName = Bot.get_guild(000000000000000000) #Server ID
    TimeOutMember = ServerName.get_member_named("Friend#0000") #friends Name + tag
    MemberRole1 = discord.utils.get(ServerName.roles, name="Generic Name 1")
    MemberRole2 = discord.utils.get(ServerName.roles, name="Generic Name 2")
    FriendRole = discord.utils.get(ServerName.roles, name="Generic Name 3")

    # Prints that bot is ready for use
    print(f'{Bot.user.name} is connected!')
        
# Removes friends "Funny Name" Role
@Bot.command(name="Naughty")
async def TimeOut(ctx, *args):
    global EndTime

    # Set arg to provided input, or default value if empty
    if args == ():
        arg = 5 # Defaults to 5 mins
    else:
        arg = "".join(args)

    # Determines friend isn't on time out
    if TimeOutMember.roles[1] != FriendRole:
        # Get time out length from command
        try:
            TimeOutLength = round(abs(float(arg))) #Remove decimals and negatives
        except:
            TimeOutLength = int(1440) # 24 hours, AKA Max time out length
        
        if TimeOutLength > 1440:
            TimeOutLength = 1440 # 24 hours, AKA Max time out length

        # Sends time out message
        if TimeOutLength < 1440:
            await ctx.channel.send(f"Again? Really? Guess they're on time out... they'll be gone for {TimeOutLength//60} hours {TimeOutLength%60} minutes. ")
        else:
            await ctx.channel.send("What? Hmm... I suppose they can go on time out for 24 hours. ")
        
        # Sets Roles
        await TimeOutMember.remove_roles(MemberRole1, MemberRole2)
        await TimeOutMember.add_roles(FriendRole)
        WasNice = False # Define before use

        # Commences Wait
        EndTime = datetime.now() + timedelta(minutes=TimeOutLength)
        while EndTime > datetime.now():
            await asyncio.sleep(0.1)
            if TimeOutMember.roles[1] != FriendRole: # Breaks if Nice command run
                WasNice = True
                break
            continue

        # Resets Roles
        if WasNice == False: # Skips if already done by Nice command
            await ctx.channel.send(f"After {TimeOutLength//60} hours {TimeOutLength%60} minutes, friends back from timeout! If they can behave... ")
            await TimeOutMember.remove_roles(FriendRole)
            await TimeOutMember.add_roles(MemberRole1, MemberRole2)

    # Message for if already on time out
    else:
        await ctx.channel.send("friends already on time out.")


# Removes friends "Funny Name" Role
@Bot.command(name="Nice")
async def TimeIn(ctx):

    # Message for if friend tries to use on himself
    if ctx.author == TimeOutMember:
        await ctx.channel.send("Nice try friend! But you're still on time out.")

    # Determines friend is already on time out
    elif TimeOutMember.roles[1] == FriendRole:

        # Resets Roles
        await TimeOutMember.remove_roles(FriendRole)
        await TimeOutMember.add_roles(MemberRole1, MemberRole2)
        await ctx.channel.send("friends back from time out early! If they can behave... ")

    # Message for if not on time out
    else:
        await ctx.channel.send("friends not on time out.")


# States if/how long friends on time out for
@Bot.command(name="Timeout")
async def TimeLeft(ctx):

    # Determines friend is already on time out
    if TimeOutMember.roles[1] == FriendRole:

        # Determines time left on time out, the returns to channel
        TimeRemaining = EndTime - datetime.now()
        RemainingHours = TimeRemaining.days * 24 + TimeRemaining.seconds // 3600
        RemainingMinutes = (TimeRemaining.seconds % 3600) // 60
        RemainingSeconds = TimeRemaining.seconds % 60
        await ctx.channel.send(f"friend is on timeout for {RemainingHours} hours, {RemainingMinutes} minutes and {RemainingSeconds} seconds.")

    # Message for if not on time out
    else:
        await ctx.channel.send("friends not on time out.")


# Runs bot using unique bot token
Bot.run("MTAwNTIwNzYwMDIzNDc1ODE2Nw.GdBvwV.6pNaVgtsoDd85wnGxkZ0jKlgUdFAO8W2mhfHpM")
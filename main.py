# Definietly the most shitty bot in github history
# You can hate it in any way but idc
# The most important part in it is that it actually works
import requests
import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions
import sqlite3
import asyncio

def getprefix(client, message):

    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT prefix FROM info WHERE guild_id = {message.guild.id}")
    result = cursor.fetchone()
    if result == None:
        prefix = "$"
    else:
        prefix = result
    cursor.close()
    db.close()
    return prefix

intents = discord.Intents.default()
intents.members = True 
intents.messages = True

# Set $ as bot prefix
client = commands.Bot(command_prefix=getprefix, intents = intents)
# Remove default command
client.remove_command("help")

# Define what happend when the bot is ready
@client.event
async def on_ready():
    print("""
    =======================================
    PY-Finder bot successfully logged in!
    =======================================
    Made by bremu45#4077
    =======================================

    Errors:
    
    """)

    # Main settings database connect
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS info(guild_id INT, prefix STR)")
    cursor.close()
    db.close()

    await client.change_presence(activity=discord.Streaming(name=f"$help to get help", url="https://www.twitch.tv/esl_csgo"))     





#███╗░░██╗░█████╗░██████╗░███╗░░░███╗░█████╗░██╗░░░░░
#████╗░██║██╔══██╗██╔══██╗████╗░████║██╔══██╗██║░░░░░
#██╔██╗██║██║░░██║██████╔╝██╔████╔██║███████║██║░░░░░
#██║╚████║██║░░██║██╔══██╗██║╚██╔╝██║██╔══██║██║░░░░░
#██║░╚███║╚█████╔╝██║░░██║██║░╚═╝░██║██║░░██║███████╗
#╚═╝░░╚══╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝





# Define help command
@client.command(aliases = ["pomoc", "faq"])
async def help(ctx):
    await ctx.message.delete()
    helpembed = discord.Embed(title=":question: Help", colour=discord.Colour(0xf40552), description=f"""
        `$find`
            <xxxxxx>
        """)
    helpembed.set_thumbnail(url="https://cutewallpaper.org/24/think-emoji-png/emoticon-thinking-transparent-png-stickpng.png")
    helpembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=helpembed, delete_after = 15)

# Define prefix command
@client.command(aliases = ["p"])
@has_permissions(administrator=True)
async def prefix(ctx, prefix):
    await ctx.message.delete()
    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute(f"SELECT guild_id FROM info WHERE  guild_id = {ctx.author.guild.id}")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO info(guild_id, prefix) VALUES(?, ?)", (ctx.author.guild.id, prefix))
    else:
        cursor.execute("UPDATE info SET prefix = ? WHERE guild_id = ?", (prefix, ctx.author.guild.id))
    prefixembed = discord.Embed(title=":white_check_mark: Prefix changed", colour=discord.Colour(0xf40552), description=f"Successfully changed prefix to `{prefix}`")
    prefixembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    prefixembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=prefixembed, delete_after = 5)
    db.commit()
    cursor.close()
    db.close()

# Define clear command
@client.command (aliases = ["purge", "kasuj", "wyczysc"])
@commands.guild_only()
@has_permissions(manage_messages=True)
async def clear(ctx, count = 0):
    if count > 100:
        await ctx.message.delete()
        clear100embed = discord.Embed(title=":warning: Purge", colour=discord.Colour(0xf40552), description=f"You can't remove more than **100** messages!\nThis limitation is caused by Discord's policy.")
        clear100embed.set_thumbnail(url="https://freepngimg.com/save/37007-angry-emoji/512x536")
        clear100embed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=clear100embed, delete_after = 5)
        return
    await ctx.message.delete()
    await ctx.channel.purge(limit=count)
    clearembed = discord.Embed(title=":white_check_mark: Purge", colour=discord.Colour(0xf40552), description=f"Successfully cleared **{count}** messages!")
    clearembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    clearembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=clearembed, delete_after = 5)






#███████╗██╗███╗░░██╗██████╗░
#██╔════╝██║████╗░██║██╔══██╗
#█████╗░░██║██╔██╗██║██║░░██║
#██╔══╝░░██║██║╚████║██║░░██║
#██║░░░░░██║██║░╚███║██████╔╝
#╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═════╝░





# Define playing status command
@client.command(aliases = ["cfx", "fivem", "server"])
async def find(ctx, cfx):
	if "https://cfx.re/join/" in cfx:
		cfxcode = cfx[20:]
	elif "http://cfx.re/join/" in cfx:
		cfxcode = cfx[19:]
	elif "cfx.re/join/" in cfx:
		cfxcode = cfx[12:]
	elif "https://servers.fivem.net/servers/detail/" in cfx:
		cfxcode = cfx[41:]
	elif "http://servers.fivem.net/servers/detail/" in cfx:
		cfxcode = cfx[40:]	
	else:
		cfxcode = cfx

	r = requests.get(f"https://servers-frontend.fivem.net/api/servers/single/{cfxcode}", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})
	if r.text == '{"error": "404 Not Found"}':
		findnieznalembed = discord.Embed(title=":x:  Server not found", colour=discord.Colour(0xf40552), description=f"The server you specified wasn't found by the bot!")
		findnieznalembed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/jPuVkQCmDg9zmBk6xAanj4_l1gJmtnXTBVZ8XPtQxaw/https/freepngimg.com/save/37007-angry-emoji/512x536")
		findnieznalembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
		await ctx.channel.send(embed=findnieznalembed)
	else:
		r = r.json()
		ep = r['EndPoint']
		hn = r['Data']['hostname']
		onlc = r['Data']['clients']
		maxc = r['Data']['sv_maxclients']
		lc = r['Data']['vars']['locale']
		svl = r['Data']['vars']['sv_lan']
		votes = r['Data']['upvotePower']
		iv = r['Data']['iconVersion']
		ip = r['Data']['connectEndPoints'][0]
		size = len(ip)
		ipbez = ip[:size - 6]
		rip = requests.get(f"https://db-ip.com/demo/home.php?s={ipbez}")
		rip = rip.json()
		country = rip['demoInfo']['countryCode']
		city = rip['demoInfo']['city']
		isp = rip['demoInfo']['isp']
		org = rip['demoInfo']['organization']
		build = ""
		bld = requests.get(f"https://servers-frontend.fivem.net/api/servers/single/{cfxcode}", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})
		if "sv_enforceGameBuild" in bld.text:
			bld = bld.json()
			build = bld['Data']['vars']['sv_enforceGameBuild']
		else:
			build = "1604"

		findznalembed = discord.Embed(title=":white_check_mark:  Server found", colour=discord.Colour(0xf40552), description=f"\nCode: `{ep}`\nHostname: `{hn}`\nSlots: `{onlc}/{maxc}`\nBuild: `{build}`\nLocale: `{lc}`\nsv_lan: `{svl}`\nVotes: `{votes}`\n\n\n/info.json: [Click here](http://{ip}/info.json)\n/players.json [Click here](http://{ip}/players.json)\n/dynamic.json [Click here](http://{ip}/dynamic.json)\n\n\nIP: `{ip}`\nCountry: `{country}`\nCity: `{city}`\nISP: `{isp}`\nOrganization: `{org}`\n")
		findznalembed.set_thumbnail(url=f"https://servers-live.fivem.net/servers/icon/{ep}/{iv}.png")
		findznalembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
		await ctx.channel.send(embed=findznalembed)









#░██████╗████████╗░█████╗░████████╗██╗░░░██╗░██████╗
#██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║░░░██║██╔════╝
#╚█████╗░░░░██║░░░███████║░░░██║░░░██║░░░██║╚█████╗░
#░╚═══██╗░░░██║░░░██╔══██║░░░██║░░░██║░░░██║░╚═══██╗
#██████╔╝░░░██║░░░██║░░██║░░░██║░░░╚██████╔╝██████╔╝
#╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░░╚═════╝░╚═════╝░





# Define playing status command
@client.command(aliases = ["graj", "playing"])
@commands.cooldown(1, 5, commands.BucketType.member)
@has_permissions(administrator=True)
async def play(ctx, *, game):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=game))
    playingembed = discord.Embed(title=":white_check_mark: Playing", colour=discord.Colour(0xf40552), description="Successfully set the playing status for the bot!\nStatus: **"+game+"**")
    playingembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    playingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=playingembed, delete_after = 5)

# Define listening status command
@client.command(aliases = ["sluchaj", "listening"])
@commands.cooldown(1, 5, commands.BucketType.member)
@has_permissions(administrator=True)
async def listen(ctx, *, music):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=music))
    listeningembed = discord.Embed(title=":white_check_mark: Listening", colour=discord.Colour(0xf40552), description="Successfully set the listening status for the bot!\nStatus: **"+music+"**")
    listeningembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    listeningembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=listeningembed, delete_after = 5)

# Define watching status command
@client.command(aliases = ["ogladaj", "watching"])
@commands.cooldown(1, 5, commands.BucketType.member)
@has_permissions(administrator=True)
async def watch(ctx, *, video):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=video))
    watchingembed = discord.Embed(title=":white_check_mark: Watching", colour=discord.Colour(0xf40552), description="Successfully set the watching status for the bot!\nStatus: **"+video+"**")
    watchingembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    watchingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=watchingembed, delete_after = 5)

# Define competing status command
@client.command(aliases = ["competing"])
@commands.cooldown(1, 5, commands.BucketType.member)
@has_permissions(administrator=True)
async def compete(ctx, *, compete):
    await ctx.message.delete()
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=compete))
    watchingembed = discord.Embed(title=":white_check_mark: Competing", colour=discord.Colour(0xf40552), description="Successfully set the watching status for the bot!\nStatus: **"+compete+"**")
    watchingembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    watchingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=watchingembed, delete_after = 5)

# Define streaming status command
@client.command(aliases = ["streamuj", "streaming"])
@commands.cooldown(1, 5, commands.BucketType.member)
@has_permissions(administrator=True)
async def stream(ctx, *, stream):
    await ctx.message.delete()
    await client.change_presence(activity=discord.Streaming(name=stream, url="https://www.twitch.tv/esl_csgo"))
    streamingembed = discord.Embed(title=":white_check_mark: Streaming", colour=discord.Colour(0xf40552), description="Successfully set the streaming status for the bot!\nStatus: **"+stream+"**")
    streamingembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
    streamingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
    await ctx.channel.send(embed=streamingembed, delete_after = 5)


# Define status command
@client.command()
@commands.guild_only()
@commands.has_role(945471691969150977)
async def status(ctx, address):
    if (ctx.channel.id == 946239873914925098):
        await ctx.message.delete()
        r = requests.get(f'https://api.mcsrvstat.us/2/{address}')
        r = r.json()
        status = r['online']
        ip = r['ip']
        port = r['port']
        if (status == True):
            version = r['version']
            protocol = r['protocol']
            onlineplayers = r['players']['online']
            maxplayers = r['players']['max']
            statussuccessembed = discord.Embed(title="Status: 🟢", colour=discord.Colour(0xf40552), description=f"IP: **{ip}:{port}**\nVersion: **{version}**\nProtocol: **{protocol}**\nSlots: **{onlineplayers}/{maxplayers}**")
            statussuccessembed.set_thumbnail(url="https://www.nicepng.com/png/full/32-324680_like-emoji-smiley-face-thumbs-up.png")
            statussuccessembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
            await ctx.channel.send(embed=statussuccessembed, delete_after = 7.5)
        else:
            statuserrorembed = discord.Embed(title="Status: 🔴", colour=discord.Colour(0xf40552), description=f"Server is offline")
            statuserrorembed.set_thumbnail(url="https://cdn.kurwa.club/files/3VLyp.png")
            statuserrorembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
            await ctx.channel.send(embed=statuserrorembed, delete_after = 7.5)





#███████╗██████╗░██████╗░░█████╗░██████╗░░██████╗
#██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝
#█████╗░░██████╔╝██████╔╝██║░░██║██████╔╝╚█████╗░
#██╔══╝░░██╔══██╗██╔══██╗██║░░██║██╔══██╗░╚═══██╗
#███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║██████╔╝
#╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═════╝░





@play.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        playmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$play <something>`")
        playmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        playmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=playmissingembed, delete_after = 5)

@watch.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        watchmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$watch <something>`")
        watchmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        watchmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=watchmissingembed, delete_after = 5)

@listen.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        listenmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$listen <something>`")
        listenmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        listenmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=listenmissingembed, delete_after = 5)

@compete.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        listenmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$compete <something>`")
        listenmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        listenmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=listenmissingembed, delete_after = 5)

@stream.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        streammissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$stream <something>`")
        streammissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        streammissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=streammissingembed, delete_after = 5)

@clear.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        clearmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$clear <count>`")
        clearmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        clearmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=clearmissingembed, delete_after = 5)

@prefix.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        clearmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$prefix <prefix>`")
        clearmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        clearmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=clearmissingembed, delete_after = 5)

@find.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        statusmissingembed = discord.Embed(title=":warning: Missing required arguments", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$find <xxxxxx>`")
        statusmissingembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        statusmissingembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=statusmissingembed, delete_after = 5)
    if isinstance(error, commands.BadArgument):
        await ctx.message.delete()
        statusbadembed = discord.Embed(title=":warning: Bad arguments provided", colour=discord.Colour(0xf40552), description=f"Correct command usage: `$find <xxxxxx>`")
        statusbadembed.set_thumbnail(url="https://www.pngmart.com/files/12/Thinking-Emoji-PNG-Photos.png")
        statusbadembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=statusbadembed, delete_after = 5)
    if isinstance(error, commands.MissingRole):
        await ctx.message.delete()
        statusroleembed = discord.Embed(title=":warning: Insufficient permissions", colour=discord.Colour(0xf40552), description=f"You don't have permissions to use this command!")
        statusroleembed.set_thumbnail(url="https://freepngimg.com/save/37007-angry-emoji/512x536")
        statusroleembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=statusroleembed, delete_after = 5)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        commandnotfoundembed = discord.Embed(title=":warning: Command not found", colour=discord.Colour(0xf40552), description=f"The command you provided doesn't exist!")
        commandnotfoundembed.set_thumbnail(url="https://freepngimg.com/save/37007-angry-emoji/512x536")
        commandnotfoundembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=commandnotfoundembed, delete_after = 5)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.delete()
        commandcooldownembed = discord.Embed(title=":warning: You are on cooldown!", colour=discord.Colour(0xf40552), description=f"You are using this command too fast! Try again in **{error.retry_after:.1f}s**!")
        commandcooldownembed.set_thumbnail(url="https://freepngimg.com/save/37007-angry-emoji/512x536")
        commandcooldownembed.set_footer(text="PY-Finder", icon_url="https://cdn.kurwa.club/files/PvE1i.png")
        await ctx.channel.send(embed=commandcooldownembed, delete_after = 5)




























































































#████████╗░█████╗░██╗░░██╗███████╗███╗░░██╗
#╚══██╔══╝██╔══██╗██║░██╔╝██╔════╝████╗░██║
#░░░██║░░░██║░░██║█████═╝░█████╗░░██╔██╗██║
#░░░██║░░░██║░░██║██╔═██╗░██╔══╝░░██║╚████║
#░░░██║░░░╚█████╔╝██║░╚██╗███████╗██║░╚███║
#░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝





# Login to the bot
client.run("OTYzNzI0OTMwNTYwNzEyNzQ0.YlaQyA.IAEZIAjWhGCBglKfmKxUpttccW4")
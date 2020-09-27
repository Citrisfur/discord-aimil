# bot.py
import os, discord, asyncio, discord.utils, calendar, re, requests, datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='a!')
bot.remove_command('help')

@bot.event
async def on_ready():
	global illusoria
	illusoria = bot.guilds[0]
	print(f"Aimil was properly initalized at {str(datetime.datetime.now())}")

@bot.command(name='help')
async def help(ctx, command=''):
    print(f"help command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
    header = '''
All commands for Aimil begin with the prefix 'a!'. Most commands are also formatted into user-friendly strings, instead of returning primital values.
In the usage statements, parameters specified with {curly braces} required, while (parenthesis) are optional.
For any issues, please contact @Citrisfur#0404, or nathanscoy@gmail.com.
'''
    commandList = {
        "help": '''
help // Displays a list of commands that Aimil can recognize.
    Usage: a!help (command)
    [string] command - specifies a command to display additional information about.''',
        "ping": '''
ping // Returns the bot's latency in seconds.
    Usage: a!ping''',
    }

    if command != '':
        if command.lower() in commandList:
            await ctx.send(header + commandList[command.lower()])
        else:
            await ctx.send("The specified command doesn't exist. Recheck the typing, or try the command list with a!help.")
    else:
        await ctx.send(header + '''
=== Command List ===

help
ping
tech
joined
echo

== Moderator ==

giverole
removerole
removeintro

= Debugging =

wikitest
listemoji
modcheck
''')

@bot.command(name='ping')
async def ping(ctx):
    print(f"ping command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
    await ctx.send(f"Aimil is latent by {str(bot.latency)} seconds.")

@bot.command(name="wikitest", help="a way to test the wiki's status")
async def wikitest(ctx):
	print(f"wikitest command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	page = requests.get("http://ichno.org/illusoria/doku.php?id=players:citrisfur")
	pageText = page.text
	output = "Testing on Citrisfur's wiki page:\nInformation as it appears on the wiki:\n"

	result = re.search("Join date:.+>(.+)<", pageText)
	output += "Citrisfur's join date: " + result.group(1) + '\n'

	result = re.search("DoB:.+>(.+)</td><", pageText)
	output += "Citrisfur's DoB: " + result.group(1) + '\n'

	result = re.search("Timezone:.+>(.+)<", pageText)
	output += "Citrisfur's time zone: " + result.group(1) + '\n'
	await ctx.send(output)

@bot.command(name="tech", help="retrieves a tech from the wiki")
async def tech(ctx, techName):
	print(f"tech command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	await ctx.trigger_typing()
	pageNum = 1
	pages = {
		1: "dark",
		2: "earth",
		3: "fire",
		4: "light",
		5: "oz",
		6: "water",
		7: "wind",
		8: "no_element"
	}

	result = None
	while result == None:
		page = requests.get("http://ichno.org/illusoria/doku.php?id=lore:techniques:" + pages[pageNum] + "&do=edit")
		pageText = page.text
		result = re.search("^.+" + techName + ".+\|", pageText, flags=re.M+re.I)
		pageNum += 1
		if pageNum == 9:
			break

	if result != None:
		await ctx.send("**Tech:** " + techName.capitalize() + ' ' + ctx.author.mention + "\n```fix\n^  Stage  ^  Technique  ^  Range/Targets  ^  Style  ^  Element  ^  Power  ^  Other Information  ^  Description  ^  Evo. From  ^```\n```" + result.group(0).replace("&quot;", "\"") + "```")
	else:
		await ctx.send(ctx.author.mention + " Tech " + techName + " not found in the wiki.")

@bot.command(name="listemoji", help="lists all server emojis")
async def listemoji(ctx):
	print(f"listemoji command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	emojiList = ''
	i = 0
	for emoji in illusoria.emojis:
		emojiList += emoji.name + ": " + str(emoji) + ", "
		i += 1
		if i == 20:
			await ctx.send(emojiList[:-2])
			emojiList = ''
			i = 0

	await ctx.send(emojiList[:-2])

@bot.command(name="joined", help="displays the date and time of a user's join")
async def joined(ctx, name=''):
	print(f"joined command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	if name == '':
		name = ctx.author.name
	member = await illusoria.query_members(query=name, limit=1, user_ids=None, cache=True)
	if member != []:
		joinTime = str(member[0].joined_at)
		await ctx.send(member[0].name + " joined Illusoria on " + calendar.month_name[int(joinTime[6:7])] + " " + joinTime[9:10] + ", " + joinTime[0:4] + " at " + joinTime[12:] + " UTC.")
	else:
		await ctx.send("Member not found.")

@bot.command(name='echo', help="returns the user's argument")
async def echo(ctx, msg):
	print(f"echo command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	await ctx.send(msg)

@bot.command(name="giverole")
async def giverole(ctx, addingRole, person):
	print(f"giverole command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	for role in illusoria.roles:
		if str(addingRole) in role.name:
			addingRole = role
			break

	member = await illusoria.query_members(query=person, limit=1, user_ids=None, cache=True)
	if member == []:
		await ctx.send(f"Member {person} not found.")
	else:
		await member[0].add_roles(illusoria.get_role(addingRole.id))
		await ctx.send(f"{member[0].name} now has the {illusoria.get_role(addingRole.id).name} role.")

@bot.command(name="removerole")
@commands.has_role("Mod Gestapo")
async def removerole(ctx, removingRole, person):
	print(f"removerole command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	removeRole = removingRole
	member = await illusoria.query_members(query=person, limit=1, user_ids=None, cache=True)
	for role in member[0].roles:
		if str(removingRole) in role.name:
			removeRole = role
			break

	if removeRole == removingRole:
		await ctx.send(member[0].name + " does not have the role.")
		return

	await member[0].remove_roles(illusoria.get_role(removeRole.id))
	await ctx.send(member[0].name + " no longer has the role " + illusoria.get_role(removeRole.id).name + ".")

@bot.command(name="removeintro")
async def removeintro(ctx, person):
	print(f"removeintro command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	confirmCheck = True
	confirm = ''

	async for intro in bot.get_channel(737087582764269635).history():
		if person in intro.author.name.lower():
			await ctx.send(f"intro by {intro.author.name} found. delete this intro? y/n")
			while confirmCheck:
				confirm = await bot.wait_for('message')
				if confirm.author == ctx.author:
					confirmCheck = False

			if confirm.content == 'y':
				await intro.delete()
				await ctx.send(f"intro by {intro.author.name} was deleted.")
				break
			else:
				await ctx.send("intro was not deleted.")
				confirmCheck = True

	if confirm == '':
		await ctx.send(f"no intros by user {person} were found.")

@bot.command(name="modcheck")
@commands.has_role("Mod Gestapo")
async def modcheck(ctx):
	print(f"modcheck command was run by {str(ctx.author)} at {str(datetime.datetime.now())}")
	await ctx.send("pass")

@bot.event
async def on_command_error(ctx, error):
	usages = {
		"joined": "Usage: a!joined {user-name}",
		"giverole": "Usage: a!giverole {role-name} {user-name}",
		"removerole": "Usage: a!removerole {role-name} {user-name}",
		"removeintro": "Usage: a!removeintro {user-name}",
	}

	if isinstance(error, commands.errors.MissingRequiredArgument):
		await ctx.send(usages.get(ctx.invoked_with))
	elif isinstance(error, commands.errors.CheckFailure):
		await ctx.send("You do not have the mod role.")
	else:
		await ctx.send(str(error))

bot.run(TOKEN)

###########################################
# WhoRU Discord Bot
# See which celebrity you look like!
###########################################

from recognise_face import lookup
from os import remove

###########################################
# UUID Generator
###########################################
from random import choice
from string import ascii_letters, digits


def uuid_char():
	""" Get a random character in the alphabet string."""
	return choice(ascii_letters + digits)

def make_uuid(length = 16):
	""" Join a bunch of characters of the length variable length.
		Those characters are called individually from the method "uuid_char"
	"""
	return ''.join([uuid_char() for _ in range(length)])

###########################################
# Loading variables
###########################################
from os import getenv
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
PREFIX = getenv("PREFIX")

###########################################
# Initialising discord bot
###########################################
from discord import File
from discord.ext import commands

bot = commands.Bot(command_prefix = PREFIX)

@bot.event
async def on_ready():
	print("Bot is online")

###########################################
# Comamnds
###########################################

image_types = ["png", "jpeg", "jpg"]

@bot.command()
async def who(ctx):
	if len(ctx.message.attachments) == 0:
		return await ctx.reply("No attachments given.")

	# Dictionary which contains the array of files to their respective UUID.
	filesToUUID = {}

	# Iterating through attachments and saving them, deleting later.
	for attachment in ctx.message.attachments:
		if not attachment.filename.lower().split(".")[-1] in image_types:
			continue

		extension = f".{attachment.filename.split('.')[-1]}"

		filesToUUID[attachment.filename] = make_uuid() + extension
		await attachment.save(f"temporary-images/{uuid}{extension}")

	# Iterating through attachments and saying who it looks like
	for file in filesToUUID:
		name = lookup(f"temporary-images/{filesToUUID[file]}")

		if not name:
			await ctx.reply("No faces in image.")
		elif name == ">1":
			await ctx.reply("More than 1 face in image.")
		else:
			face_file = File(f"faces/{name}.jpg")
			await ctx.reply(
				f"The picture you sent (apparently) looks like {name}",
				file = face_file
			)
		
		# Delete the attachment after I'm finished with it.
		remove(f"temporary-images/{filesToUUID[file]}")

###########################################
# Inserting token
###########################################
bot.run(DISCORD_TOKEN)

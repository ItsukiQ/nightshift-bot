import discord
from discord.ext import commands
from discord import app_commands
import json
import os

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.message_content = True

# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user.name} ({bot.user.id})")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))	
	
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} command(s)")
	except Exception as e:
		print(f"Failed to sync commands: {e}")
	

@bot.tree.command(name="join", description="Make the bot join your current voice channel")
async def join(interaction: discord.Interaction):
	if not interaction.user.voice:
		await interaction.response.send_message(
			"hala wala ka sa call teh",
			ephemeral=True
		)
		return
	
	vc = interaction.user.voice.channel
	if interaction.guild.voice_client:
		await interaction.response.send_message(
			"nasa call na ako gurl kalma",
			ephemeral=True
		)
		return
	
	# try to join the VC
	try:
		voice_client = await vc.connect()
		await interaction.response.send_message(
			f"Joined {vc.name}! di ako aalis hanggang di niyo ko ipa /leave sige kayo"
		)
		print(f"Connected to voice channel: {vc.name}")
	except Exception as e:
		print(f"Error joining voice channel: {e}")
		await interaction.response.send_message(
			"di ako teh nakajoin sorry",
			ephemeral=True
		)


@bot.tree.command(name="leave", description="Make the bot leave the voice channel")
async def leave(interaction: discord.Interaction):
	if not interaction.guild.voice.client:
		await interaction.guild.voice_client(
			"wala ako sa vc ano ba",
			ephemeral=True
		)

	await interaction.guild.voice_client.disconnect()
	await interaction.response.send_message("Nag-left n q ng VC.")

	print("Disconnected from voice channel.")


@bot.event
async def on_voice_state_update(member, before, after):
	if member.id == bot.user.id:
		if before.channel and not after.channel:
			print("Nightshift Bot was disconnected from the voice channel.")

bot.run(token)
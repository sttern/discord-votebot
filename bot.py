Python 3.13.2 (main, Feb  5 2025, 08:05:21) [GCC 14.2.1 20250128] on linux
Type "help", "copyright", "credits" or "license()" for more information.
>>> import discord
... from discord.ext import commands
... import asyncio
... import os
... from dotenv import load_dotenv
... 
... load_dotenv()
... TOKEN = os.getenv("DISCORD_BOT_TOKEN")
... 
... intents = discord.Intents.default()
... intents.messages = True
... intents.guilds = True
... intents.dm_messages = True
... intents.members = True  # Required to DM members
... 
... bot = commands.Bot(command_prefix="!", intents=intents)
... 
... votes = {}  # Stores votes (user_id -> choice)
... 
... @bot.event
... async def on_ready():
...     print(f'Logged in as {bot.user}')
... 
... @bot.command()
... @commands.has_permissions(administrator=True)
... async def startvote(ctx, *, question):
...     """Starts a vote and DMs all members."""
...     global votes
...     votes.clear()
...     await ctx.send(f"Starting vote: {question}\nCheck your DMs to vote!")
...     
...     for member in ctx.guild.members:
...         if not member.bot:
...             try:
...                 await member.send(f"Vote: {question}\nReply with your choice.")
...             except:
...                 print(f"Couldn't DM {member}")
... 
... @bot.event
... async def on_message(message):
...     """Handles DMs for voting."""
...     if message.guild is None and message.author != bot.user:
...         if message.author.id not in votes:
...             votes[message.author.id] = message.content.strip()
...             await message.channel.send("Your vote has been recorded!")
...         else:
...             await message.channel.send("You've already voted!")
...     await bot.process_commands(message)
... 
... @bot.command()
... @commands.has_permissions(administrator=True)
... async def results(ctx):
...     """Shows vote results."""
...     if not votes:
...         await ctx.send("No votes recorded yet.")
...         return
...     
...     results_count = {}
...     for choice in votes.values():
...         results_count[choice] = results_count.get(choice, 0) + 1
...     
...     results_text = "\n".join(f"{choice}: {count} votes" for choice, count in results_count.items())
...     await ctx.send(f"Vote Results:\n{results_text}")

bot.run(TOKEN)

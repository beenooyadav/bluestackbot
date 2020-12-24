import os

import google_search
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='google', help='top five links')
async def google(ctx, *query):
    print(f'query: {query}')
    response = '\n'.join(google_search.get_top5_google_result(query))
    print(f'response: {response}')
    await ctx.send(response)


@bot.command(name='recent', help='recent searches')
async def recent(ctx, *query):
    print(f'query: {query}')
    response = '\n'.join(google_search.recent_search_result(query))
    print(f'response: {response}')
    await ctx.send(response)


@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == 'hi':
        response = 'Hey'
        await message.channel.send(response)

bot.run(TOKEN)

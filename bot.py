# bot.py
import os
import random
import logging
# 22
import discord
from dotenv import load_dotenv
from discord.ext import commands

from openweather import get_local_weather

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("bot.log"),  # Log to a file
                        logging.StreamHandler()            # Log to console
                    ])

bot = commands.Bot(command_prefix='/',intents=intents)

# Command to respond with a random quote
@bot.command(name='helpMe', help='Responds with a list of commands')
async def quote(ctx):
    supp_commands = [
        '/helpMe -> prints out commands',
        '/quote -> prints out random quote',
        '/yourIp -> prints out public ip',
        '/localWeatherNow -> prints out local weather now',
        '/localWeatherForecast -> prints out local weather forecast',
        '/whoIsAlive -> prints out who are alive in homelab',
        '/99 -> prints out random quote from Brooklyn 99'
    ]
    #response = random.choice(quotes)
    await ctx.send(f"Here is a list of supported commands:")
    for i in supp_commands:
        await ctx.send(i)

# Command to respond with a random quote
@bot.command(name='quote', help='Responds with a random quote')
async def quote(ctx):
    print(f"{ctx.author.name} sent: {ctx.message.content}")
    quotes = [
        '“The only thing we have to fear is fear itself.” – Franklin D. Roosevelt ',
        '“To be, or not to be, that is the question.” – William Shakespeare ',
        'The future belongs to those who believe in the beauty of their dreams.',
        '“The future belongs to those who believe in the beauty of their dreams.” – Eleanor Roosevelt ',
        '“That which does not kill us makes us stronger.” – Friedrich Nietzsche ',
        '“Knowledge is power.” – Francis Bacon',
        '“A journey of a thousand miles begins with a single step.” – Lao Tzu ',
        '“The greatest glory in living lies not in never falling, but in rising every time we fall.” – Nelson Mandela ',
        '“It is better to have loved and lost than never to have loved at all.” – Alfred Tennyson',
        '“Ask not what your country can do for you, ask what you can do for your country.” – John F. Kennedy',
        '“A small leak will sink a great ship.” – Benjamin Franklin ',
        '“It is better to light a single candle than to curse the darkness.” – Confucius (Advocating for action over negativity)',
        '“You miss 100% of the shots you don’t take.” – Wayne Gretzky ',
        '“Curiosity killed the cat, but satisfaction brought it back.” – Eugene O’Neill ',
        '“The pen is mightier than the sword.” – Edward Bulwer-Lytton',
        '“Life is what happens when you’re busy making other plans.” – John Lennon'

    ]
    response = random.choice(quotes)
    await ctx.send(response)

@bot.command(name='yourIp', help='Responds with current public ip')
async def public_ip(ctx):
    import urllib.request
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    response = external_ip
    await ctx.send(f"My ip is: {response}")

@bot.command(name='whoIsAlive', help='Responds with table what machines are up in network')
async def whoisalive(ctx):
    ip_dictionary = {
        "Gateway": "172.31.5.5",
        "PiHole": "172.31.5.35",
        "NUC11_eth": "172.31.5.30",
        "NUC11_wifi": "172.31.5.31",
        "filesrv": "172.31.5.33",
        "jellyfin_eth": "172.31.5.25",
        "jellyfin_wifi": "172.31.5.41",
        "zbook_eth": "172.31.5.26",
        "zbook_wifi": "172.31.5.32",
    }
    await ctx.send(f"Here's list of connection statuses in homelab:")
    for ip in ip_dictionary:
        response = os.popen(f"ping {ip_dictionary[ip]}").read()
        # Pinging each IP address 4 times
        if response.count("unreachable") != 0 or response.count("timed out") != 0:
            # print(f"❌ {ip} Ping Unsuccessful, Host is DOWN.")
            #ping_results[ip] = "❌ - DOWN"
            await ctx.send(f"❌ {ip} Status is DOWN")
        else:
            # print(f"✅ {ip} Ping Successful, Host is UP!")
            #ping_results[ip] = "✅ - UP"
            await ctx.send(f"✅ {ip} Status is UP")
    await ctx.send(f"-- END --")

@bot.command(name='localWeatherNow', help='Responds with local weather')
async def local_weather_now(ctx):
    result = get_local_weather(req_type="now")
    await ctx.send(f"Local weather in:")
    for ip in result:
        await ctx.send(f"{ip} is: {result[ip]}")

@bot.command(name='localWeatherForecast', help='Responds with local weather forecast')
async def local_weather_forecast(ctx):
    result = get_local_weather(req_type="forecast")
    await ctx.send(f"Here's local weather forecast in Ylöjärvi:")
    for ip in result:
        await ctx.send(f"{ip} is: {result[ip]}")
    await ctx.send(f"-- END --")

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

# Handle commands that are not defined
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry, I don't recognize that command: `{ctx.message.content}`. Please try again!")
        print(f"{ctx.author.name} sent an unrecognized command: {ctx.message.content}")
        logging.warning(f"{ctx.author.name} sent an unrecognized command: {ctx.message.content}")


bot.run(TOKEN)
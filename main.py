import os
import discord

my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in successfully as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # TODO: reformat this to have instructions
  if msg.startswith("!hello"):
    await message.channel.send(
      "Hello, world! This will eventually be updated with instructions on how to get instructions!"
    )


client.run(os.getenv('TOKEN'))

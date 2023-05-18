import os
import discord
from mymodule import new_character_handler
from classes import Character


async def new_character(ctx):
  #Get server ID from discord API
  server_id = ctx.guild.id

  #remove bot command
  input_string = ctx.message.content.lower().split()
  args = input_string[1:]
  args.append(str(server_id))
  #sanitize
  sanitized_character = "".join(ch for ch in " ".join(args)
                                if ch.isalnum() or ch.isspace() or ch == "-")

  # dictioanry for new character
  keys = [
    'first_name', 'last_name', 'skin', 'level', 'hot', 'cold', 'volatile',
    'dark', 'server_id'
  ]
  values = sanitized_character.split()

  new_character = {keys[i]: values[i] for i in range(len(keys))}

  new_character['first_name'] = new_character['first_name'].capitalize()
  new_character['last_name'] = new_character['last_name'].capitalize()
  new_character['skin'] = new_character['skin'].capitalize()
  new_character['level'] = int(new_character['level'])
  new_character['hot'] = int(new_character['hot'])
  new_character['cold'] = int(new_character['cold'])
  new_character['volatile'] = int(new_character['volatile'])
  new_character['dark'] = int(new_character['dark'])
  new_character['server_id'] = str(new_character['server_id'])

  #check to see if input is valid
  if len(args) != 9:
    await ctx.send(
      f"No new character has been made. Make sure you're putting it in the right order. \n Usage: {prefix}add_character <first name> <last name> <skin> <level> <hot> <cold> <volatile> <dark>. \n Note: if you are trying to add a new NPC, use {prefix}new_npc instead."
    )
    return

  result = (new_character_handler(new_character))

  # Send new character as a confirmation message
  #TODO: actually include stat block TODO: add a more helpful error message
  if result:
    await ctx.send(
      f'''{new_character['first_name']} {new_character['last_name']} the {new_character['skin']} has been added to the game!'''
    )
  else:
    await ctx.send("fail")

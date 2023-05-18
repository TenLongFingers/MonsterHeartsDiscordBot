import os
import discord
from discord.ext import commands
import string

import random
from custom_modules.dice_roller_handlers import get_character_stat_handler

exclamations_array = [
  "WOW!", "HOLY SH*T!", "F*CK YEAH!", "HOT DAMN!", "ya-YEET!", "POG!", "(⊙０⊙)",
  "ᕦ༼ ˵ ◯ ਊ ◯ ˵ ༽ᕤ"
]

exclamation = random.choice(exclamations_array)
fail_msg = ":poop:"

big_success = range(10, 26)
avg_success = range(7, 10)
failed_roll = range(-16, 7)

## FUNCTIONS##
#TODO: add the stats as a callback function. Then you can do an if/elif statements in the roll function, so they can choose whether or not to roll stats


# BASIC 2D6
def basic_roll_dice(ctx, stat):
  dice_1 = random.randint(1, 6)
  dice_2 = random.randint(1, 6)
  total = dice_1 + dice_2

  return total, dice_1, dice_2


#ROLL STAT COMMAND
def roll_command(ctx, server_id, *args):

  #rolls just a basic 2D6
  if len(args) == 0:
    #TODO: add ifs, so exclamations are added if it's a big success
    total, dice_1, dice_2 = basic_roll_dice(ctx, None)
    response = f'''You rolled {dice_1} and {dice_2} for a total of {total}'''
    return response

  #rolls a 2D6 plus a stat value
  else:
    name = args[0]
    stat_name = args[1]
    total, dice_1, dice_2 = basic_roll_dice(ctx, stat_name)
    stat_int = get_character_stat_handler(server_id, name, stat_name)
    if stat_int is not None:
      total += stat_int

    #Allows user to add a custom modifier to a roll
    if len(args) == 3:
      try:
        modifier = int(args[2])
        total += modifier
      except ValueError:
        response = f'''Is {modifier} a real number? Because I can't seem to get it to add...I'm sorry!'''
        return response

  if stat_name is not None:
    response = f'''{name} rolled {dice_1} and {dice_2} using {stat_name} for a total of {total}'''
    return response
  else:
    response = f'''Could not find a stat called {stat_name} for {name}. Was everything spelled right?'''
    print(stat_int, stat_name)
    return response


#   # Random exclamations for super successes
#   exclamation = random.choice(exclamations_array)
#   if msg.startswith(prefix + "roll"):
#     total, dice_1, dice_2 = basic_roll_dice()
#     result = "You rolled " + str(dice_1) + " and " + str(
#       dice_2) + " for a total of " + str(total)

# Messages for different rolls TODO: these will probably have to be moved to a different function so people can add stats. It'll have to be restructured.
# if total == 2:
#   result = (":poop:  ") + result + ("! FAIL!")
# elif 3 <= total <= 6:
#   result = ("Fail! ") + result + (".")
# elif 7 <= total <= 9:
#   result = ("Success! ") + result + (".")
# elif total > 9:
#   result = (exclamation + " " + result + ("! SUCCESS!!"))

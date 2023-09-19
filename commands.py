import random
import discord
import asyncio
import requests
import json
import helpers
import datetime
from replit import db

async def coinflip(client, message):
  channel = message.channel
  embed = discord.Embed(title='Coinflip', \
                        description='vote first :^)\n You have 30 Seconds to choose ⌛', \
                        color=0x00EAFF)
  coin_emojis = ['👑','📖']
  coin_messages = ['Heads!!!! 👑', 'Tails!!!! 📖']
  rand = random.randint(0, 1)
  
  coin_emoji = coin_emojis[rand]
  coin_message = coin_messages[rand]
  
  voting_message = await channel.send(embed=embed)
  for emoji in ['👑', '📖', '➡️']:
    await voting_message.add_reaction(emoji)
  
  def check(reaction, user):
      return reaction.message.id == voting_message.id and str(reaction.emoji) == '➡️' and reaction.count >= 2


  
  try:
      await client.wait_for('reaction_add', timeout=30.0, check=check)
  except asyncio.TimeoutError:
      await channel.send('Sorry time is up, Game is over kid :^)')
  else:
      await channel.send(coin_message)
      m = await channel.fetch_message(voting_message.id)
      winners = []
      async for user in m.reactions[rand].users():
        winners.append(user)
      if (len(winners) > 1):
        await channel.send('Congrats to the winners!!\n' + helpers.mention_people(winners[1:]))
      else:
        await channel.send(f'Haha losers i m the only 1 who voted IS THE WINNER KIDDDDDDDDOOOOOOOOOOOOOOSSSSSSSSSSSSSS wuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuwuw', tts=True)



async def gif(channel, tokens):
    response = ''
    if len(tokens) > 2:
      await channel.send('Too many Arguements!')
      return
    
    if len(tokens) == 1:
      response = requests.get(f"https://api.otakugifs.xyz/gif?reaction={helpers.get_random_gif_reaction()}")
    elif helpers.valid_gif_reaction(tokens[1]): # means len(tokens) = 2
      response = requests.get(f"https://api.otakugifs.xyz/gif?reaction={tokens[1]}")
    else:
      await channel.send('Not a Valid reaction')
      return
    
    gif = json.loads(response.text)
    await channel.send(gif['url'])


async def quote(channel):
  response = requests.get('https://zenquotes.io/api/random')
  quote = json.loads(response.text)
  quote_text = quote[0]['q']
  quote_author = quote[0]['a']
  await channel.send(f'\"{quote_text}\" -{quote_author}')

async def make_event(client, message, tokens):
  if len(tokens) < 8:
    await message.channel.send('Number of required arguements is 4')
    return
  
  event = helpers.make_discord_event(message.channel, tokens)
  await event.start()



async def send_correct_todo(message, tokens):
  author_id = str(message.author.id)
  guild_id = str(message.guild.id)
  if len(tokens) == 1:
    await helpers.show_todo_list(message, author_id, guild_id)
    return
  if len(tokens) > 2:
    await message.channel.send('Too many Arguements!')
    return
  
  #discord deals with mentions as the following
  # <@user_id> that mentions the person
  # but @everyone is just '@everyone' so we can reserve guild id for everyone
  if tokens[1] == '@everyone':
    await helpers.show_todo_list(message, message.guild.id, message.guild.id)
    return
    
  if helpers.is_valid_userid(message, tokens[1]):
    await helpers.show_todo_list(message, tokens[1][2:-1], message.guild.id)
    return
  
  await message.channel.send('Not a correct User!')

async def add_todo_task(message, tokens):
  if len(tokens) < 2:
    await message.channel.send('incorrect Arguements!')
    return
    
  user_id = str(message.author.id)
  guild_id = str(message.guild.id)
  helpers.prepare_user('TODO', user_id, guild_id)
  
  task = ' '.join(tokens[1:])
  db['TODO'][str(guild_id) + '.' + str(user_id)].append(task)
  
  await helpers.show_todo_list(message, user_id, guild_id)

async def mark_asdone(message, tokens):
  if len(tokens) != 2:
    await message.channel.send('incorrect Arguements!')
  
  user_id = str(message.author.id)
  guild_id = str(message.guild.id)
  helpers.prepare_user('TODO', user_id, guild_id)

  index = int(tokens[1]) - 1
  task_list = db['TODO'][str(guild_id) + '.' + str(user_id)]
  if index >= len(task_list) or index < 0:
    await message.channel.send('Index Out of range')
    return

  if task_list[index].startswith('~~') and task_list[index].endswith('~~'):
    await message.channel.send('Task is already done')
    return
    
  task_list[index] = '~~' + task_list[index] + '~~'
  await helpers.show_todo_list(message, user_id, guild_id)

async def delete_task(message, tokens):
  if len(tokens) != 2:
    await message.channel.send('incorrect Arguements!')
  
  user_id = str(message.author.id)
  guild_id = str(message.guild.id)
  helpers.prepare_user('TODO', user_id, guild_id)

  index = int(tokens[1]) - 1
  task_list = db['TODO'][str(guild_id) + '.' + str(user_id)]
  if index >= len(task_list) or index < 0:
    await message.channel.send('Index Out of range')
    return

  deleted_task = db['TODO'][str(guild_id) + '.' + str(user_id)][index]
  del db['TODO'][str(guild_id) + '.' + str(user_id)][index]
  await message.channel.send(f'Task Deleted Successfully: {deleted_task}')
  await helpers.show_todo_list(message, user_id, guild_id)

async def edit_task(message, tokens):
  if len(tokens) == 2:
    await message.channel.send('incorrect Arguements!')
    return
    
  user_id = str(message.author.id)
  guild_id = str(message.guild.id)
  helpers.prepare_user('TODO', user_id, guild_id)

  index = int(tokens[1]) - 1
  task_list = db['TODO'][str(guild_id) + '.' + str(user_id)]
  if index >= len(task_list) or index < 0:
    await message.channel.send('Index Out of range')
    return
  
  task_before = db['TODO'][str(guild_id) + '.' + str(user_id)][index]
  db['TODO'][str(guild_id) + '.' + str(user_id)][index] = ' '.join(tokens[2:])
  task_after = db['TODO'][str(guild_id) + '.' + str(user_id)][index]
  await message.channel.send(f'Task Edited Successfully from {task_before} to {task_after}')
  await helpers.show_todo_list(message, user_id, guild_id)

async def send_help_message(message):
  all_commands = ['edit_task (index) (Edited Task)', 'delete_task (index)', 'mark_asdone (index)', 'add_task (task)', 'todo (mention somebody [Optional])', 'disable_schedule_vote', 'activate_schedule_vote', 'quote', 'gif (reaction)', 'coinflip']
  description = 'start any command with a \'!\' \n'
  for i in range(len(all_commands)):
    description += f'{i + 1}- {all_commands[i]}.\n'

  embed = discord.Embed(title='Help message', \
                        description=description, \
                        color=0x87CEEB)
  
  await message.channel.send(embed=embed)


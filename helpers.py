import random
import discord
import datetime
import commands
from replit import db

def mention_people(people):
  mentions = ''
  for person in people:
    mentions += person.mention + '\n'
  
  return mentions

def get_gif_reaction_choices():
  return  

def get_random_gif_reaction():
    reactions_str = get_gif_reaction_choices()
    reactions = reactions_str.split(', ')
    
    return random.choice(reactions)

def valid_gif_reaction(reaction):
  return reaction in set(get_gif_reaction_choices().split(', '))

def make_event_datetime(time_components):
  year = int(time_components[0])
  month = int(time_components[1])
  day = int(time_components[2])
  hour = int(time_components[3])
  minute = int(time_components[4])
  
  time = datetime.datetime(year, month, day, hour, minute)
  return time

def make_discord_event(channel, tokens):
  name = tokens[1]
  description = tokens[2]
  
  start_time = make_event_datetime(tokens[3:])
  end_time = start_time + datetime.timedelta(hours=1)
  data = {
          'id' : channel.id,
          'guild_id' : channel.guild.id,
          'name' : name,
          'entity_type' : 'external',
          'scheduled_start_time' : start_time.isoformat(),
          'scheduled_end_time' : end_time.isoformat(),
          'status' : discord.EventStatus.scheduled,
          'description' : description
         }
  
  event = discord.ScheduledEvent(state=discord.EventStatus.scheduled, data=data)
  
  return event

def prepare_user(observable, user_id, guild_id):
  if observable not in db.keys():
    db[observable] = dict()

  saved_userid = str(guild_id) + '.' + str(user_id)
  if user_id == guild_id:
    saved_userid = str(guild_id)
  
  user_tasks_dict = db[observable]
  if saved_userid not in user_tasks_dict.keys():
    user_tasks_dict[saved_userid] = []

def get_todo_list_string(todo_list):
  if len(todo_list) == 0:
    return 'Empty!'
    
  formatted_tasks = ''
  for i in range(len(todo_list)):
    task = str(todo_list[i])
    formatted_tasks += f'{i + 1}- {task}\n'

  return formatted_tasks

def is_valid_userid(message, user_id):
  return len(user_id) > 3 and message.guild.get_member(int(user_id[2:-1])) != None


async def show_todo_list(message, user_id, guild_id):
  server_user_id = str(guild_id) + '.' + str(user_id)
  if user_id == message.guild.id:
    server_user_id = str(guild_id)
  prepare_user('TODO', user_id, guild_id)
  
  member = message.guild.get_member(int(user_id))
  embed = discord.Embed(title=f'Todo list of {member.display_name}', \
                        description=get_todo_list_string(list(db['TODO'][server_user_id])), \
                        color=member.color)
  
  await message.channel.send(embed=embed)

import discord
import asyncio
import os
import random
import helpers
import commands
from discord.ext import tasks
from replit import db
from server import keep_alive


def run_bot():
  client = discord.Client(intents=discord.Intents.all())

  @client.event
  async def on_ready():
    print(f'We have logged in as {client.user}')

  @client.event
  async def on_member_join(member):
    channel = client.get_channel(1142164933883220151)
    await channel.send(f'WELCOME!!!!! {member.mention}')

  @client.event
  async def on_member_remove(member):
    channel = client.get_channel(237989644011044864)
    await channel.send(f'I didn\'t like him anyway, {member.mention}')

  @client.event
  async def on_scheduled_event_create(event):
    await event.channel.send(f'{event.name} was created')

  @tasks.loop(seconds=10)
  async def alarm_message():
    await client.wait_until_ready()
    embed = discord.Embed(title='Coinflip', \
                        description='vote first :^)\n You have 30 Seconds to choose ⌛', \
                        color=0x00EAFF)
    message = 'test'
    await channel.send(message)

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    message_content = message.content
    message_tokens = message_content.split()
    command = message_tokens[0].lower() if len(message_tokens) > 0 else 'NONE'
    global channel
    channel = message.channel

    if command == 'hello' or command == 'hey':
      await channel.send('Greetings Soldier!')
    elif command == 'ping':
      await channel.send('pong')
    elif command == '!coinflip':
      await commands.coinflip(client, message)
    elif command == '!quote':
      await commands.quote(channel)
    elif command == '!activate_schedule_vote':
      alarm_message.start()
    elif command == '!disable_schedule_vote':
      alarm_message.cancel()
    elif command == '!todo':
      await commands.send_correct_todo(message, message_tokens)
    elif command == '!add_task':
      await commands.add_todo_task(message, message_tokens)
    elif command == '!mark_asdone':
      await commands.mark_asdone(message, message_tokens)
    elif command == '!delete_task':
      await commands.delete_task(message, message_tokens)
    elif command == '!edit_task':
      await commands.edit_task(message, message_tokens)
    elif command == '!help':
      await commands.send_help_message(message)

  keep_alive()
  client.run(os.environ['TOKEN'])

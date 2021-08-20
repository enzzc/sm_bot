import os
import sys
import discord
import aioredis

import sm

PREFIX = 'sm_bot'

client = discord.Client()
redis = aioredis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))


@client.event
async def on_ready():
    print('Logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if client.user in message.mentions:
        s1 = await redis.srandmember(f'{PREFIX}:author1')
        s2 = await redis.srandmember(f'{PREFIX}:author2')
        sentence = sm.make_sentence(s1.decode('utf-8'), s2.decode('utf-8'))
        await message.reply(sentence)


if __name__ == '__main__':
    token = os.getenv('SM_DISCORD_TOKEN')
    if not token:
        print('Where is the token, pal? (Please, set $SM_DISCORD_TOKEN)')
        sys.exit(1)
    try:
        client.run(token)
    except discord.errors.LoginFailure:
        print('Invalid token.')
        sys.exit(1)

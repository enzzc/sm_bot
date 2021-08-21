import os
import sys
import discord
import aioredis

import sm

PREFIX = 'sm_bot'

client = discord.Client()
redis = aioredis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
print(redis)


@client.event
async def on_ready():
    print('Logged as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if client.user in message.mentions:

        if '!ping' in message.content:
            await message.channel.send('pong')
            return

        for _ in range(10):  # Try 10 times before giving up
            async with redis.pipeline() as pipe:
                s1, s2 = await (pipe.srandmember(f'{PREFIX}:author1')
                                    .srandmember(f'{PREFIX}:author2')
                                    .execute())
            sentence = sm.make_sentence(s1.decode('utf-8'), s2.decode('utf-8'))
            if sentence is not None:
                break

        # If we are unlucky and haven't found any combination that
        # makes a sentence, then we fall back to the default message.
        if sentence is None:
            sentence = "Je suis à court d'idées :smirk:"

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

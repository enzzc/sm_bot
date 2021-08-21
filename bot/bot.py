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
        print('mentions')
        async with redis.pipeline() as pipe:
            s1, s2 = await (pipe.srandmember(f'{PREFIX}:author1')
                                .srandmember(f'{PREFIX}:author2')
                                .execute())
        sentence = sm.make_sentence(s1.decode('utf-8'), s2.decode('utf-8'))
        if sentence:
            await message.reply(sentence)
        else:
            await message.reply("Je suis à court d'idées :smirk:")


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

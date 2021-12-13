import os
import sys
import random
import discord
import aioredis

import sm

PREFIX = 'sm_bot'
EMOJIS = [
    ':smirk:',
    ':thinking:',
    ':upside_down:',
    ':stuck_out_tongue:',
    ':tux:',
    ':metal:',
    ':love_letter:',
    ':drooling_face:',
    ':kissing_smiling_eyes:',
    ':kissing_heart:',
    ':heart_eyes:',
    ':star_struck:',
    ':money_mouth:',
    ':money_with_wings:',
]

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

    if client.user not in message.mentions:
        return

    if '!ping' in message.content:
        await message.channel.send('pong')
        return

    if '!stats' in message.content:
        async with redis.pipeline() as pipe:
            c1, c2 = await (pipe.scard(f'{PREFIX}:author1')
                                .scard(f'{PREFIX}:author2')
                                .execute())
        await message.channel.send(
            f'Author 1: {c1} sentences. Author 2: {c2} sentences.'
        )
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
        sentence = "Je suis à court d'idées"

    emoji = random.choice(EMOJIS)
    await message.reply(sentence + ' ' + emoji)


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

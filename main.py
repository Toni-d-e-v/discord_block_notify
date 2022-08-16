from discord.ext import commands
import json
import asyncio
import requests

bot = commands.Bot(command_prefix='!')

# check
# loop to check the json and if the new block height is greater than the current block height, then send message to users in the list
async def check(bot):
    while True:
        block_height = get_block_height()
        with open('height.json', 'r') as f:
            data = json.load(f)
        for height in data:
            if int(height) >= block_height:
                for user in data[height]:
                    owner = await bot.fetch_user(user)
                    await owner.send('New block height ' + str(block_height))
                    print('Found user ' + str(user) + ' with height ' + str(height))
                    # remove user from the list of that height
                    for user in data[height]:
                        data[height].remove(user)
                    with open('height.json', 'w') as f:
                        json.dump(data, f)
        await asyncio.sleep(1)


# crate bot
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await check(bot)

# curl https://api.blockcypher.com/v1/btc/main
def get_block_height():
    url = 'https://api.blockcypher.com/v1/btc/main'
    response = requests.get(url)
    return response.json()['height']

# bot command to record block height in which they want bot to message them to notify them of the new block height
@bot.command(pass_context=True)
async def record(ctx, height):
    # check if hight is the same as the current block height
    if int(height) < get_block_height():
        await ctx.send('This block was mined')
        return
    # height.json create "height" key and create empty list
    with open('height.json', 'r') as f:
        data = json.load(f)
    if str(height) not in data:
        data[str(height)] = []
    # add user id to list of users to be notified of new block height
    data[str(height)].append(ctx.message.author.id)
    print(data)
    with open('height.json', 'w') as f:
        json.dump(data, f)
    await ctx.send('You will be notified of new block height ' + height)


loop = asyncio.get_event_loop()
asyncio.ensure_future(bot.run('ODMwODU2MjE1Nzk3MzAxMjQ4.GVL_nB.Lec3nyo8AoKz1XJdZgE70VFg6gGLRCcgRY3guQ'))
loop.run_forever()
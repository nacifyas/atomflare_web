import discord
from discord.ext import commands, ipc


class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "test")

    async def on_ready(self):
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("Ipc server is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


bot_client = Bot(command_prefix = "!", intents = discord.Intents.default())


@bot_client.ipc.route()
async def get_guild_count(data):
    return len(my_bot.guilds) # returns the len of the guilds to the client

@bot_client.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in my_bot.guilds:
        final.append(guild.id)
    return final # returns the guild ids to the client


@bot_client.command()
async def hi(ctx):
    await ctx.send("Hi")

bot_client.ipc.start()
bot_client.run("TOKEN")
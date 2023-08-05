
import discord

async def send_message(message, user_message, is_private, responses):
    try:
        response = responses.function(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
def run_discord_bot(TOKEN):
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_text = str(message.content)
        channel = str(message.channel)
        if user_text[0] == '$':
            user_text = user_text[1:]  # [1:] Removes the '$'
            await send_message(message, user_text, is_private=True)
        else:
            await send_message(message, user_text, is_private=False)


    
    client.run(TOKEN)
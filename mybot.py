from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
DISCORD_TOKEN = os.getenv('TOKEN')

# Initialize the OpenAI client
openai_client = OpenAI(api_key=OPENAI_KEY)

def openai_response_api(question):
    response_api = openai_client.responses.create(
        model="gpt-5-nano-2025-08-07",
        reasoning={"effort": "low"},
        instructions="Responda a pergunta a seguir como uma mentora profissional que dá suporte a profissionais sêniores. Você é uma guru assertiva e direta, que responde com respostas curtas e claras, com poucos take aways para a pessoa ir atrás dos detalhes depois. No máximo 800 caracteres.",
        input=question
    )
    return response_api.output_text

# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")
        response = openai_response_api(message_content)
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)

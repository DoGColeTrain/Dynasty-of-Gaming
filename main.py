import openai
import discord
from discord.ext import commands
import 

# 🔹 OpenAI API initialisieren
openai.api_key = OPENAI_API_KEY

# 🔹 Discord-Bot Einstellungen mit erweiterten Berechtigungen
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 📌 Speichert aktive Gespräche
active_users = set()

# 🔹 Funktion für ChatGPT-Antworten
def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Du bist ein hilfreicher Discord-Bot."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Fehler: {e}"

# 📌 1️⃣ Befehl `!chat` startet das Gespräch
@bot.command(name="ai")
async def chat(ctx, *, message: str):
    """Startet das Gespräch und erlaubt Folgefragen ohne `!chat`."""
    response = chatgpt_response(message)
    await ctx.send(f"🤖 **Bot:** {response}")
    active_users.add(ctx.author.id)  # Nutzer zur aktiven Liste hinzufügen

# 📌 2️⃣ Befehl `!stop` beendet das Gespräch
@bot.command(name="off")
async def stop(ctx):
    """Beendet das Gespräch, sodass der Bot nicht mehr automatisch antwortet."""
    if ctx.author.id in active_users:
        active_users.remove(ctx.author.id)
        await ctx.send(f"🚫 **{ctx.author.name}, das Gespräch wurde beendet.**")
    else:
        await ctx.send(f"ℹ️ **{ctx.author.name}, du hast kein aktives Gespräch.**")

# 📌 3️⃣ Der Bot antwortet direkt, wenn jemand zuvor `!chat` genutzt hat
@bot.event
async def on_message(message):
    """Antwortet auf Nachrichten, wenn der Nutzer zuvor `!chat` genutzt hat."""
    if message.author == bot.user:
        return  # Verhindert, dass der Bot auf sich selbst antwortet

    if message.author.id in active_users:
        response = chatgpt_response(message.content)
        await message.channel.send(f"🤖 **Bot:** {response}")

    await bot.process_commands(message)  # Andere Befehle bleiben aktiv

# 📌 4️⃣ Bot startet und meldet sich in der Konsole
@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

bot.run(DISCORD_BOT_TOKEN)

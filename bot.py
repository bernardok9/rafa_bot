import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

PREFIXO_LINK = "https://gamersclub.com.br/j/"

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")

@bot.command()
#@commands.has_permissions(manage_messages=True)
async def preview(ctx, limite: int = 100):
    try:
        await ctx.message.delete()
    except:
        pass
    mensagens = []

    async for msg in ctx.channel.history(limit=limite):
        if msg.content.startswith(PREFIXO_LINK):
            mensagens.append(msg)

    if not mensagens:
        await ctx.send("Não achei nenhuma mensagem, seu imbecil 👍.", delete_after=8)
        return

    max_preview = min(limite, len(mensagens), 40)

    texto = "\n".join(m.content for m in mensagens[:max_preview])

    await ctx.send(
        f"Aqui seu animal {max_preview} de {len(mensagens)} mensagens:\n```{texto}```", delete_after=20
    )

    ctx.bot.mensagens_para_apagar = mensagens


@bot.command()
async def confirmar(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    mensagens = getattr(ctx.bot, "mensagens_para_apagar", [])

    if not mensagens:
        await ctx.send("Tu é burro? já apaguei seu merda 👍.")
        return

    apagadas = 0
    for msg in mensagens:
        try:
            await msg.delete()
            apagadas += 1
        except:
            pass

    ctx.bot.mensagens_para_apagar = []
    
    await ctx.send(f"👍 {apagadas} apagadas, agora cala boca, ta mutado 😡.", delete_after=10)
    
@bot.command()
async def limpar_tudo(ctx, limite: int = 100):
    try:
        await ctx.message.delete()
    except:
        pass

    apagadas = 0
    

    async for msg in ctx.channel.history(limit=limite):
        if msg.content.startswith(PREFIXO_LINK):
            try:
                await msg.delete()
                apagadas += 1
            except:
                pass

    await ctx.send(
        f"Hard me lambuzou {apagadas} vezes 🥵.",
        delete_after=5
    )

bot.run(TOKEN)

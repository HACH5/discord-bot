import discord, asyncio
from discord import app_commands
import os, datetime
from dotenv import load_dotenv
import btc
import openai
import time

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "gpt-3.5-turbo"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def check_is_me(ctx: discord.Interaction):
    return ctx.user.id == int(os.getenv("DISCORD_ID"))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="HADABot"))
    print("-----------------------------------")
    print("Bot is ready.")
    print("-----------------------------------")
    await tree.sync()
    print("Syncを実行しました")
    print("-----------------------------------")

# 参加しているサーバー表示
@tree.command(
    name="gl",
    description="hadadayoだけが動かせるコマンド"
)

@app_commands.check(check_is_me)
async def showguild(ctx: discord.Interaction):
    count_server = len(client.guilds)
    guildlist = discord.Embed(title="参加しているサーバーList", description=f"合計：{count_server}サーバー")
    for guild in client.guilds:
        guildlist.add_field(name="サーバー名：", value=f"{guild}", inline=False)
    await ctx.response.send_message(embed=guildlist, ephemeral=True)


@showguild.error
async def showguild_error(ctx: discord.Interaction, error):
    await ctx.response.send_message(f"{ctx.user.mention}さんは権限がありません")

# @tree.command(name="test", description="testです")
# async def test_command(interaction: discord.Interaction):
#     await interaction.response.send_message("test!", ephemeral=True)

@tree.command(name="graph", description="BTCの直近(1ヵ月)のグラフを表示します。")
async def graph(interaction: discord.Interaction):
    jpy = btc.get_btc_graph()
    embed=discord.Embed(title="BitCoin")
    embed.add_field(name=f"現在{int(jpy):,}円", value="多少誤差はあります", inline=False)
    embed.add_field(name="↓直近1ヵ月のグラフ", value="⚠グラフの値段はUSD表記です", inline=False)
    file = discord.File(f"img/BTC_price.png",f"BTC_price.png")
    embed.set_image(url="attachment://BTC_price.png")
    await interaction.response.send_message(embed=embed, file=file)

@tree.command(name="chat", description="お話をしましょう！")
async def chat(interaction: discord.Interaction, text:str):
    try:
        await interaction.response.defer()
        completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {
                    "role": "system",
                    "content": "日本語で返答"
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
        )
        res = completion["choices"][0]["message"]["content"]
        await interaction.followup.send(res)
    except:
        import traceback
        traceback.print_exc()
        await interaction.response.send_message("エラーが発生しました")


client.run(TOKEN)
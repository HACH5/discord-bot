import discord
from discord import app_commands
import os, datetime
from dotenv import load_dotenv
import btc

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def check_is_me(ctx: discord.Interaction):
    return ctx.user.id == int(os.getenv("DISCORD_ID"))


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


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="HADABot"))
    print("-----------------------------------")
    print("Bot is ready.")
    print("-----------------------------------")
    await tree.sync()
    print("Syncを実行しました")
    print("-----------------------------------")

@client.event
async def on_guild_join():
    count_server = len(client.guilds)
    print("-----------------------------------")
    print('新しくサーバーに追加されました。')
    print(f"現在参加しているサーバー数：{count_server}")
    print("-----------------------------------")
    for guild in client.guilds:
        print(guild.name)
    print("-----------------------------------")

@tree.command(name="test", description="testです")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("test!", ephemeral=True)

@tree.command(name="graph", description="グラフを表示します。")
async def graph(interaction: discord.Interaction):
    btc.get_btc_graph()
    embed=discord.Embed(title="BTC(直近1ヵ月)")
    file = discord.File(f"img/BTC_price.png",f"BTC_price.png")
    embed.set_image(url="attachment://BTC_price.png")
    await interaction.response.send_message(embed=embed, file=file)


client.run(TOKEN)
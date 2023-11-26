import discord, asyncio
from discord import ui, app_commands
from discord.interactions import Interaction
from discord.ui import Select, View
import os, datetime
from dotenv import load_dotenv
import btc
import openai
import time
import traceback
import genshin
import logging

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "gpt-3.5-turbo"

intents = discord.Intents.default()
client = discord.Client(intents=intents, help_command=None)
tree = app_commands.CommandTree(client)

handler = logging.FileHandler(filename='log/discord.log', encoding='utf-8', mode='w')

GUILD_ID = discord.Object(1087992275302350860)

class search_name_artifact(ui.Modal, title="聖遺物検索"):
    result = discord.ui.TextInput(label="検索する文字を入力して下さい", placeholder="聖遺物の名前のキーワードを打ってね", default="絶縁")
    async def on_submit(self, interaction: discord.Interaction):
        index = 1
        res = genshin.search_name_artifact(str(self.result))
        # print(res)
        if len(res) <= 6:
            embed = discord.Embed(title="聖遺物検索", description=f"{self.result}の検索結果{len(res)}件見つかりました")
            for artifact in res:
                embed.add_field(name=f"{index}件目:聖遺物の詳細", value=f"名前:{artifact[3]}")
                embed.add_field(name=f"{artifact[3]}のレアリティ", value=f"☆{artifact[1]}")
                embed.add_field(name=f"{artifact[3]}の2セット効果", value=f"{artifact[6]}", inline=False)
                embed.add_field(name=f"{artifact[3]}の4セット効果", value=f"{artifact[7]}", inline=False)
                index += 1
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="聖遺物検索", description=f"{self.result}の検索結果{len(res)}件見つかりましたが、内容を省略して表示します")
            for artifact in res:
                embed.add_field(name=f"{index}件目:聖遺物の詳細", value=f"名前:{artifact[3]}")
                embed.add_field(name=f"{artifact[3]}のレアリティ", value=f"☆{artifact[1]}")
                index += 1
            await interaction.response.send_message(embed=embed)

class search_status_artifact(ui.Modal, title="聖遺物検索"):
    result = discord.ui.TextInput(label="検索する文字を入力して下さい", placeholder="4セットの効果で検索しています", default="元素熟知")
    async def on_submit(self, interaction: discord.Interaction):
        res = genshin.search_status_artifact(str(self.result))
        # print(res)
        if len(res) <= 6:
            embed = discord.Embed(title="聖遺物検索", description=f"{self.result}の検索結果{len(res)}件見つかりました")
            for artifact in res:
                embed.add_field(name=f"{index}件目:聖遺物の詳細", value=f"名前:{artifact[3]}")
                embed.add_field(name=f"{artifact[3]}のレアリティ", value=f"☆{artifact[1]}")
                embed.add_field(name=f"{artifact[3]}の2セット効果", value=f"{artifact[6]}", inline=False)
                embed.add_field(name=f"{artifact[3]}の4セット効果", value=f"{artifact[7]}", inline=False)
                index+=1
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="聖遺物検索", description=f"{self.result}の検索結果{len(res)}件見つかりましたが、内容を省略して表示します")
            for artifact in res:
                embed.add_field(name=f"{index}件目:聖遺物の詳細", value=f"名前:{artifact[3]}")
                embed.add_field(name=f"{artifact[3]}のレアリティ", value=f"☆{artifact[1]}")
            await interaction.response.send_message(embed=embed)


class search_name_character(ui.Modal, title="キャラクター検索"):
    result = discord.ui.TextInput(label="検索する名前の文字を入力して下さい", placeholder="名前のキーワードを打ってね", default="クレー")
    async def on_submit(self, interaction: discord.Interaction):
        index = 1
        res = genshin.search_name_character(str(self.result))
        # print(res)
        if len(res) <= 6:
            embed = discord.Embed(title="キャラクター検索", description=f"{self.result}の検索結果{len(res)}件見つかりました")
            for character in res:
                embed.add_field(name=f"{index}件目:キャラクターの詳細", value=f"名前:{character[2]}", inline=False)
                embed.add_field(name=f"{character[2]}のレアリティ", value=f"☆{character[3]}", inline=False)
                embed.add_field(name=f"{character[2]}の元素", value=f"{genshin.search_element_name(character[4])[0][0]}", inline=False)
                embed.add_field(name=f"{character[2]}の誕生日", value=f"{character[5]}", inline=False)
                embed.add_field(name=f"{character[2]}の出身場所", value=f"{genshin.search_place_name(character[6])[0][0]}", inline=False)
                index+=1
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="キャラクター検索", description=f"{self.result}の検索結果{len(res)}件見つかりましたが、内容を省略して表示します")
            for character in res:
                embed.add_field(name=f"{index}件目:キャラクターの詳細", value=f"名前:{character[2]}")
                embed.add_field(name=f"{character[2]}のレアリティ", value=f"☆{character[3]}")
                embed.add_field(name=f"{character[2]}の元素", value=f"{genshin.search_element_name(character[4])[0][0]}")
            await interaction.response.send_message(embed=embed)
            
class search_birthday_character(ui.Modal, title="キャラクター検索"):
    result = discord.ui.TextInput(label="検索する誕生日を入力して下さい", placeholder="月/日と検索してください。月/, /日でもOK")
    async def on_submit(self, interaction: discord.Interaction):
        index = 1
        res = genshin.search_birthday_character(str(self.result))
        # print(res)
        if len(res) <= 8:
            embed = discord.Embed(title="キャラクター検索", description=f"{self.result}の検索結果{len(res)}件見つかりました")
            for character in res:
                embed.add_field(name=f"{index}件目:キャラクターの詳細", value=f"名前:{character[2]}", inline=False)
                embed.add_field(name=f"{character[2]}のレアリティ", value=f"☆{character[3]}")
                embed.add_field(name=f"{character[2]}の誕生日", value=f"{character[5]}")
                index+=1
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="キャラクター検索", description=f"{self.result}の検索結果{len(res)}件見つかりましたが、8件しか表示ができません")
            for character in res:
                embed.add_field(name=f"{index}件目:キャラクターの詳細", value=f"名前:{character[2]}", inline=False)
                embed.add_field(name=f"{character[2]}のレアリティ", value=f"☆{character[3]}")
                embed.add_field(name=f"{character[2]}の誕生日", value=f"{character[5]}")
                index+=1
                if(index == 9):
                    break
            await interaction.response.send_message(embed=embed)

class search_chara_artifact_name(ui.Modal, title="検索結果"):
    result = discord.ui.TextInput(label="検索する文字を入力して下さい", placeholder="キャラクターの名前を入力して下さい", default="胡桃")
    async def on_submit(self, interaction: discord.Interaction):
        try:
            index = 1
            res = genshin.search_chara_artifact_name(str(self.result))
            embed = discord.Embed(title="検索結果", description=f"{self.result}の検索結果{len(res)}件見つかりました")
            embed.add_field(name=f"キャラクター名", value=f"名前:{res[0][0]}")
            embed.add_field(name=f"{res[0][0]}のレアリティ", value=f"☆{res[0][1]}")
            embed.add_field(name=f"{res[0][0]}の元素", value=f"{res[0][2]}")
            for types in res:
                embed.add_field(name=f"{index}つ目", value=f"種類名:{types[3]}")
                embed.add_field(name=f"{types[3]}:聖遺物の名前", value=f"名前:{types[4]}")
                embed.add_field(name=f"時の砂のメインステータス", value=f"{types[5]}", inline=False)
                embed.add_field(name=f"空の杯のメインステータス", value=f"{types[6]}", inline=False)
                embed.add_field(name=f"理の冠のメインステータス", value=f"{types[7]}", inline=False)
                index+=1
            await interaction.response.send_message(embed=embed)
        except:
            traceback.print_exc()
            await interaction.response.send_message("エラーが発生しました")

class search_chara_artifact_artifact(ui.Modal, title="検索結果"):
    result = discord.ui.TextInput(label="検索する文字を入力して下さい", placeholder="聖遺物の名前を入力して下さい", default="金メッキ")
    async def on_submit(self, interaction: discord.Interaction):
        try:
            index = 1
            res = genshin.search_chara_artifact_artifact(str(self.result))
            if len(res) <= 3:
                embed = discord.Embed(title="検索結果", description=f"{self.result}の検索結果{len(res)}件見つかりました")
                for chara in res:
                    embed.add_field(name=f"キャラクター名", value=f"名前:{chara[0]}")
                    embed.add_field(name=f"{chara[0]}のレアリティ", value=f"☆{chara[1]}")
                    embed.add_field(name=f"{chara[0]}の元素", value=f"{chara[2]}")
                    embed.add_field(name=f"{chara[0]}つ目", value=f"種類名:{chara[3]}")
                    embed.add_field(name=f"{chara[3]}:聖遺物の名前", value=f"名前:{chara[4]}")
                    embed.add_field(name=f"時の砂のメインステータス", value=f"{chara[5]}", inline=False)
                    embed.add_field(name=f"空の杯のメインステータス", value=f"{chara[6]}", inline=False)
                    embed.add_field(name=f"理の冠のメインステータス", value=f"{chara[7]}", inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="検索結果", description=f"{self.result}の検索結果{len(res)}件見つかりましたが、件数が多いため情報を省略して表示します")
                for chara in res:
                    embed.add_field(name=f"{chara[0]}", value=f"種類名:{chara[3]}")
                embed.add_field(name="もっと詳しく調べる↓", value="/chara_artifactコマンドの名前検索で調べてください", inline=False)
                await interaction.response.send_message(embed=embed)
        except:
            traceback.print_exc()
            await interaction.response.send_message("エラーが発生しました")

def check_is_me(interaction: discord.Interaction):
    return interaction.user.id == int(os.getenv("DISCORD_ID"))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="HADABot"))
    print("-----------------------------------")
    print("Bot is ready.")
    print("-----------------------------------")
    await tree.sync()
    await tree.sync(guild=GUILD_ID)
    print("Syncを実行しました")
    print("-----------------------------------")


# 参加しているサーバー表示
@tree.command(name="gl",description="hadadayoだけが動かせるコマンド")
@app_commands.check(check_is_me)
async def showguild(interaction: discord.Interaction):
    count_server = len(client.guilds)
    guildlist = discord.Embed(title="参加しているサーバー", description=f"合計：{count_server}サーバー")
    await interaction.response.send_message(embed=guildlist, ephemeral=True)


@showguild.error
async def showguild_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f"{interaction.user.mention}さんは権限がありません", ephemeral=True)

# @tree.command(name="test", description="testです")
# async def test_command(interaction: discord.Interaction):
#     await interaction.response.send_message("test!", ephemeral=True)

@tree.command(name="test", description="test")
@discord.app_commands.guilds(GUILD_ID)
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("test!", ephemeral=True)

@tree.command(name="stop", description="Botの停止コマンド")
@app_commands.check(check_is_me)
async def stop_command(interaction: discord.Interaction):
    await interaction.response.send_message("Botを停止します", ephemeral=True)
    print("!------------------------------!")
    print("終了コマンドが入力されました")
    print("!------------------------------!")
    await client.close()

@stop_command.error
async def stop_command_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f"{interaction.user.mention}さんは権限がありません", ephemeral=True)

@tree.command(name="graph", description="BTCの直近(1ヵ月)のグラフを表示します。")
async def graph(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        jpy = btc.get_btc()
        embed=discord.Embed(title="BitCoin")
        embed.add_field(name=f"現在{int(jpy):,}円", value="多少誤差はあります", inline=False)
        embed.add_field(name="↓直近1ヵ月のグラフ", value="⚠グラフの値段はUSD表記です", inline=False)
        file = discord.File(f"img/BTC_price.png",f"BTC_price.png")
        embed.set_image(url="attachment://BTC_price.png")
        await interaction.followup.send(embed=embed, file=file)
    except:
        traceback.print_exc()
        await interaction.response.send_message("エラーが発生しました")

@tree.command(name="chat", description="お話をしましょう！")
@app_commands.describe(text="お話ししたい内容を入力してください")
async def chat(interaction: discord.Interaction, text:str):
    await interaction.response.defer()
    try:
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
        traceback.print_exc()
        await interaction.followup.send("エラーが発生しました")
    

@tree.command(name="artifact", description="聖遺物を検索することができます")
async def artifact(interaction: discord.Interaction):
    select = Select(options=[
        discord.SelectOption(label="名前",
                             value="name",
                             description="名前で検索"
                             ),

        discord.SelectOption(label="聖遺物の効果",
                             value="status",
                             description="聖遺物の効果で検索")
    ])

    async def artifact_callback(interaction):
        if select.values[0] == "name":
            await interaction.response.send_modal(search_name_artifact())
        if select.values[0] == "status":
            await interaction.response.send_modal(search_status_artifact())
    

    select.callback = artifact_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message("聖遺物検索", view=view)

@tree.command(name="character", description="現在操作可能であるキャラクターを検索することができます")
async def character(interaction: discord.Interaction):
    select = Select(options=[
        discord.SelectOption(label="名前",
                             value="name",
                             description="名前で検索"
                             ),

        discord.SelectOption(label="誕生日",
                             value="birthday",
                             description="誕生日で検索")
    ])

    async def character_callback(interaction):
        if select.values[0] == "name":
            await interaction.response.send_modal(search_name_character())
        if select.values[0] == "birthday":
            await interaction.response.send_modal(search_birthday_character())
    

    select.callback = character_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message("キャラクター検索", view=view)

@tree.command(name="chara_artifact", description="キャラクターに最適な聖遺物を表示します")
async def character(interaction: discord.Interaction):
    select = Select(options=[
        discord.SelectOption(label="名前",
                             value="name",
                             description="名前で検索"
                             ),

        discord.SelectOption(label="聖遺物",
                             value="artifact",
                             description="聖遺物で検索")
    ])

    async def character_callback(interaction):
        if select.values[0] == "name":
            await interaction.response.send_modal(search_chara_artifact_name())
        if select.values[0] == "artifact":
            await interaction.response.send_modal(search_chara_artifact_artifact())
    

    select.callback = character_callback
    view = View()
    view.add_item(select)
    await interaction.response.send_message("聖遺物検索", view=view)

@tree.command(name="support", description="エラーなど発生した場合の問い合わせ場所")
async def support_command(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.gg/35h9EZ46gF に参加し、チケットを作成の上お知らせください。お手数ですがよろしくお願いします。", ephemeral=True)

client.run(TOKEN, log_handler=handler)

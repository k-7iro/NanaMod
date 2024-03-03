from AI_Gemini import set_token, call_ai, token_id
from nextcord.ext import menus, commands
import nextcord
import json

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

config = {}
with open("serverconfigs.json", "r") as f:
    config = json.loads(f.read())

tokens = {}
with open("tokens.json", "r") as f:
    tokens = json.loads(f.read())

@bot.event
async def on_ready():
    set_token(tokens[token_id])
    print(f'{bot.user}としてログイン完了。')

@bot.event
async def on_message(message):
    if bot.user.id in [member.id for member in message.mentions]:
        if message.reference == None:
            embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.dark_red())
            embed.add_field(name="エラー", value="対象のメッセージに対して返信する形でNanaModをメンションしてください。", inline=False)
            await message.channel.send(embed=embed)
        else:
            if str(message.guild.id) in config and "rule" in config[str(message.guild.id)]:
                msg = await message.channel.fetch_message(message.reference.message_id)
                if msg.author == bot.user:
                    embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.dark_red())
                    embed.add_field(name="エラー", value="NanaModに対してNanaModを使うことはできません。", inline=False)
                    await message.channel.send(embed=embed)
                else:
                    async with message.channel.typing():
                        response = call_ai("メッセージがルールに違反している場合は「可能性あり」「中程度の違反」「重大に違反」の三つのカテゴリーから適切なものを言ってください。理由も付けてください。違反していない場合は「OK」とだけ言ってください。\nメッセージ："+msg.content+"\nルール："+config[str(message.guild.id)]["rule"])
                        ename = msg.content
                        print("Raw Response: "+response+"\nメッセージ："+msg.content+"\nルール："+config[str(message.guild.id)]["rule"])
                        if len(ename) > 256:
                            ename = ename[:253]+"..."
                        if response == "OK":
                            embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.green())
                            try:
                                embed.set_author(name=ename, icon_url=msg.author.avatar.url)
                            except:
                                pass
                            embed.add_field(name="判定", value="このメッセージはルールに違反していません。", inline=False)
                            embed.add_field(name="注意", value="この判定はAIが下したものであり、正確とは限りません。あくまでも判断材料としてご利用ください。", inline=False)
                        else:
                            split_response = response.split("\n")
                            try:
                                embed.set_author(name=ename, icon_url=msg.author.avatar.url)
                            except:
                                pass
                            if split_response[0] == "可能性あり":
                                embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.yellow())
                                embed.add_field(name="判定", value="このメッセージはルールに違反している可能性があります。", inline=False)
                                embed.add_field(name="理由", value="".join(split_response[1:]), inline=False)
                            elif split_response[0] == "中程度の違反":
                                embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.orange())
                                embed.add_field(name="判定", value="このメッセージはルール違反をしています。", inline=False)
                                embed.add_field(name="理由", value="".join(split_response[1:]), inline=False)
                            elif split_response[0] == "重大に違反":
                                embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.red())
                                embed.add_field(name="判定", value="このメッセージは重大なルール違反をしています。", inline=False)
                                embed.add_field(name="理由", value="".join(split_response[1:]), inline=False)
                            else:
                                embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.dark_red())
                                embed.add_field(name="判定", value="このメッセージはエラーで違反レベルを得られませんでしたが、おそらく違反しています。", inline=False)
                                embed.add_field(name="理由", value="".join(split_response), inline=False)
                            embed.add_field(name="注意", value="この判定はAIが下したものであり、正確とは限りません。あくまでも判断材料としてご利用ください。", inline=False)
                        await message.channel.send(embed=embed)
            else:
                embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.dark_red())
                embed.add_field(name="エラー", value="ルールが設定されていません。/set_ruleコマンドでルールを設定してください。", inline=False)
                await message.channel.send(embed=embed)

@bot.slash_command(description="NanaModに適応させるルールを変更します")
async def set_rule(ctx, rule:str):
    try:
        config.setdefault(str(ctx.guild_id), {})
        config[str(ctx.guild_id)]["rule"] = rule
        with open("serverconfigs.json", "w") as f:
            f.write(json.dumps(config))
    except:
        embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.red())
        embed.add_field(name="エラー", value="ルールの設定に失敗しました。しばらくたった後にもう一度試すか、公式サポートサーバーにてお問い合わせください。", inline=False)
    else:
        embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.green())
        embed.add_field(name="成功", value="ルールを設定しました。", inline=False)
    await ctx.send(embed=embed)

@bot.slash_command(description="NanaModに適応させるルールを変更します")
async def get_rule(ctx):
    if config[str(ctx.guild.id)] and config[str(ctx.guild.id)]["rule"]:
        embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.green())
        embed.add_field(name="ルール", value=config[str(ctx.guild.id)]["rule"], inline=False)
    else:
        embed = nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.red())
        embed.add_field(name="エラー", value="ルールが設定されていません。", inline=False)
    await ctx.send(embed=embed)

@bot.slash_command(description="一括チェックします")
async def bulk_check(ctx, messages:int):
    await ctx.response.defer()
    msgs = await ctx.channel.history(limit=messages).flatten()
    info = await ctx.send("チェック中です (0/"+str(messages)+") ... これには数分かかることがあります。")
    cnt = 0
    bcnt = 1
    ecnt = 0
    embeds = []
    embeds.append(nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.blue()))
    embeds[0].add_field(name="一括判定", value="以下のメッセージがルール違反を検出しました：", inline=False)
    for i in msgs:
        cnt += 1
        if not (i.author.bot or i.content == ""):
            try:
                response = call_ai("メッセージがルールに違反している場合は「可能性あり」「中程度の違反」「重大に違反」の三つのカテゴリーから適切なものを言ってください。理由も付けてください。違反していない場合は「OK」とだけ言ってください。\nメッセージ："+i.content+"\nルール："+config[str(ctx.guild.id)]["rule"])
            except:
                ecnt += 1
            else:
                if response != "OK":
                    bcnt += 1
                    ename = i.author.name+": "+i.content
                    if len(ename) > 256:
                        ename = ename[:253]+"..."
                    embeds[len(embeds)-1].add_field(name=ename, value="理由："+response, inline=False)
                    if bcnt == 25:
                        bcnt = 0
                        embeds.append(nextcord.Embed(title="NanaMod", description="V2.0 by K-Nana", color=nextcord.Color.blue()))
            try:
                await info.edit(content="チェック中です ("+str(cnt)+"/"+str(messages)+") ... これには数分かかることがあります。")
            except:
                pass
    embeds[len(embeds)-1].add_field(name="注意", value=str(ecnt)+"件のメッセージでエラーが発生しました。\nこの判定はAIが下したものであり、正確とは限りません。あくまでも判断材料としてご利用ください。", inline=False)
    for i in embeds:
        await ctx.channel.send(embed=i)

bot.run(tokens["discord"])

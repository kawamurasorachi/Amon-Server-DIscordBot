import os
import sys
from dotenv import load_dotenv
import discord
import sympy
from PIL import Image
from datetime import datetime

load_dotenv(override=True)

client = discord.Client()
vcn_channel = 826055515243151380  # None
amg_channel = None
hakaba_channel = 850389307394883654  # None
main_channel = 815782299076657188  # None
is_notification = True
game_id = ''
game_card = None
mute_card = None
game_member = []
game_member_is_muted = []
mute_member = []
emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣',
         '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟️']


@client.event
async def on_message(message):
    global vcn_channel
    global amg_channel
    global is_notification
    global game_id
    global game_card
    global mute_card
    global game_member
    global emoji
    global game_member_is_muted
    global hakaba_channel
    global main_channel

    if message.author == client.user:
        return

    if message.content.split()[0] == '/help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                   "/amg_help ： AmongUsサポートコマンド一覧を表示 \n" +
                                   "/tex_help ： TexBot機能説明を表示 \n")

    if message.content.split()[0] == '/vcn_help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                   "/vcn_stop ： VC通知を停止 \n" +
                                   "/vcn_start ： VC通知を開始 \n" +
                                   "/vcn_change_channel ： VC通知チャンネルを変更 \n")

    if message.content.split()[0] == '/vcn_stop':
        if is_notification == True:
            is_notification = False
        print(is_notification)
        await message.channel.send('VC通知を停止しました')

    if message.content.split()[0] == '/vcn_start':
        if is_notification == False:
            is_notification = True
        print(is_notification)
        await message.channel.send('VC通知を開始しました')

    if message.content.split()[0] == '/vcn_change_channel':
        vcn_channel = message.channel.id
        await message.channel.send(f'VC通知チャンネルを#{message.channel}に変更しました。')

    if message.content.split()[0] == '/amg_help':
        await message.channel.send("/amg_help ： AmongUsサポートコマンド一覧を表示 \n" +
                                   "/amg_muteon ： 会議チャンネル全員をミュート \n" +
                                   "/amg_muteoff ： 会議チャンネル全員をミュート解除 \n" +
                                   "/amg_start <ルームID> ： AmongUs AutoManagerを起動 \n" +
                                   "/amg_stop： AmongUs AutoManagerを終了 \n")

    if message.content.split()[0] == '/amg_muteon':
        for i in message.author.voice.channel.members:
            await i.edit(mute=True)

    if message.content.split()[0] == '/amg_muteoff':
        for i in message.author.voice.channel.members:
            await i.edit(mute=False)

    if message.content.split()[0] == '/amg_start':
        amg_channel = message.channel.id
        game_id = message.content.split()[1]
        count = 1
        member_text = ''

        for member in message.author.voice.channel.members:
            game_member.append(member)
            game_member_is_muted.append(False)
            member_text += f'{emoji[count]}:{member.nick or member.name},'
            count += 1
        embed = discord.Embed(
            title=f"{message.author}がAmongUsを立てました", description=f"ID:{game_id}\n 参加者:\n{member_text}", color=0x0000ff)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/815788675605594142/853189141507473408/amongus.png')
        game_card = await message.channel.send(embed=embed)
        for i in range(len(message.author.voice.channel.members)):
            await game_card.add_reaction(emoji[i+1])
        mute_card = await message.channel.send('↓会議チャンネル全員をミュートするボタン')
        await mute_card.add_reaction("🔕")

    if message.content.split()[0] == '/amg_stop':
        for i in game_member:
            await i.edit(mute=False)
            await i.move_to(client.get_channel(main_channel))

        vcn_channel = 826055515243151380  # None
        amg_channel = None
        hakaba_channel = 850389307394883654  # None
        main_channel = 815782299076657188  # None
        is_notification = True
        game_id = ''
        game_card = None
        mute_card = None
        game_member = []
        game_member_is_muted = []
        emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣',
                 '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟️']
        await message.channel.send("ゲームが終了しました")

    if message.content.split()[0] == '/tex_help':
        await message.channel.send("/tex_help ： TexBot機能説明を表示 \n" +
                                   "\```tex \n" +
                                   "texのコード \n" +
                                   "\``` \n" +
                                   "例) \n" +
                                   "\```tex \n" +
                                   r"$\frac{b}{a}$"+" \n" +
                                   "\```")

    if '```tex' in message.content:
        if message.author.id != int(os.environ.get("CLIENT_ID")):
            pic_name = f'{datetime.now()}.png'
            sympy.init_printing(use_latex=True)
            wave_equation = message.content.split("""```tex""")[1][:-3]

            try:
                sympy.preview(wave_equation, viewer='file', filename=pic_name, euler=False,
                              dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600"])
                im = Image.open(pic_name)

                def add_margin(pil_img, top, right, bottom, left, color):
                    width, height = pil_img.size
                    new_width = width + right + left
                    new_height = height + top + bottom
                    result = Image.new(
                        pil_img.mode, (new_width, new_height), color)
                    result.paste(pil_img, (left, top))
                    return result

                im_new = add_margin(im, 50, 50, 50, 50, (255, 255, 255))
                im_new.save(pic_name, quality=95)
                file = discord.File(
                    pic_name, filename=pic_name)
                await message.channel.send(file=file)
                os.remove(pic_name)

            except Exception as e:
                print(e)
                await message.channel.send("出力に失敗しました。")


@client.event
async def on_voice_state_update(member, before, after):
    global is_notification
    global vcn_channel
    if vcn_channel == None:
        vcn_channel = client.guilds[0].text_channels[0].id
    alert_channel = client.get_channel(vcn_channel)
    if is_notification == True:
        if before.channel is None:
            embed = discord.Embed(
                title=f"{member.nick or member.name}が {after.channel.name} に参加しました", description="やっほー", color=0xff0000)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)
        elif after.channel is None:
            embed = discord.Embed(
                title=f"{member.nick or member.name}が {before.channel.name} から抜けました", description="バイバイ", color=0xff0000,)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)


@client.event
async def on_raw_reaction_add(payload):
    global game_card
    global mute_card
    global hakaba_channel
    global game_member
    global game_member_is_muted
    global mute_member
    global emoji

    if payload.user_id != int(os.environ.get("CLIENT_ID")):
        if payload.message_id == game_card.id:
            # if game_member_is_muted[emoji.index(payload.emoji.name) - 1] == False:
            # await game_member[emoji.index(payload.emoji.name) - 1].edit(mute=True)
            await game_member[emoji.index(payload.emoji.name) - 1].edit(mute=False)
            await game_member[emoji.index(payload.emoji.name) - 1].move_to(client.get_channel(hakaba_channel))
            game_member_is_muted[emoji.index(
                payload.emoji.name) - 1] = True
        if payload.message_id == mute_card.id:
            for i in payload.member.voice.channel.members:
                await i.edit(mute=True)
                mute_member.append(i)


@client.event
async def on_raw_reaction_remove(payload):
    global game_card
    global game_member
    global main_channel
    global game_member_is_muted
    global mute_member
    global emoji
    guild = await client.fetch_guild(payload.guild_id)
    print(guild.members)

    if payload.user_id != int(os.environ.get("CLIENT_ID")):
        if payload.message_id == game_card.id:
            if game_member_is_muted[emoji.index(payload.emoji.name) - 1] == True:
                # await game_member[emoji.index(payload.emoji.name) - 1].edit(mute=False)
                await game_member[emoji.index(payload.emoji.name) - 1].move_to(client.get_channel(main_channel))
                game_member_is_muted[emoji.index(
                    payload.emoji.name) - 1] = False
        if payload.message_id == mute_card.id:
            for i in mute_member:
                await i.edit(mute=False)

client.run(os.environ.get("DISCORD_TOKEN"))

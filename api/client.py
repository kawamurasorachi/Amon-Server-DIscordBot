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
is_notification = True
vcn_mute_from = 24
vcn_mute_to = 6


@client.event
async def on_message(message):
    global vcn_channel
    global amg_channel
    global is_notification
    global vcn_mute_from
    global vcn_mute_to

    if message.author == client.user:
        return

    if message.content.split()[0] == '/help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n")

    if message.content.split()[0] == '/vcn_help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                   "/vcn_stop ： VC通知を停止 \n" +
                                   "/vcn_start ： VC通知を開始 \n" +
                                   "/vcn_mute_from [数字] ： [数字]時からVC通知をミュート（デフォルトは24時） \n" +
                                   "/vcn_mute_to[数字] ： [数字]時までVC通知をミュート（デフォルトは6時） \n" +
                                   "/vcn_change_channel ： VC通知チャンネルを変更 \n")

    if message.content.split()[0] == '/vcn_stop':
        if is_notification == True:
            is_notification = False
        await message.channel.send('VC通知を停止しました')

    if message.content.split()[0] == '/vcn_start':
        if is_notification == False:
            is_notification = True
        await message.channel.send('VC通知を開始しました')

    if message.content.split()[0] == '/vcn_mute_from':
        vcn_mute_from = int(message.content.split()[1])
        await message.channel.send(f'{message.content.split()[1]}時からVC通知をミュートします')

    if message.content.split()[0] == '/vcn_mute_to':
        vcn_mute_to = int(message.content.split()[1])
        await message.channel.send(f'{message.content.split()[1]}時からVC通知をミュート解除します')

    if message.content.split()[0] == '/vcn_change_channel':
        vcn_channel = message.channel.id
        await message.channel.send(f'VC通知チャンネルを#{message.channel}に変更しました。')


@client.event
async def on_voice_state_update(member, before, after):
    global is_notification
    global vcn_channel
    global vcn_mute_from
    global vcn_mute_to

    if vcn_channel == None:
        vcn_channel = client.guilds[0].text_channels[0].id
    alert_channel = client.get_channel(vcn_channel)
    now_time = datetime.now().hour
    if now_time >= 15:
        now_time -= 15
    else:
        now_time += 9
    if is_notification == True and vcn_mute_from >= now_time and vcn_mute_to <= now_time:
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

client.run(os.environ.get("DISCORD_TOKEN"))

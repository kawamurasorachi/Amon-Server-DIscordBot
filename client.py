#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
import discord
from datetime import datetime
import pytz

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

    command = ''
    try:
        command = message.content.split()[0]
    except:
        command = message.content

    if message.author == client.user:
        return

    if command == '/help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n")

    if command == '/vcn_help':
        await message.channel.send("/vcn_help ： VC通知コマンド一覧を表示 \n" +
                                   "/vcn_stop ： VC通知を停止 \n" +
                                   "/vcn_start ： VC通知を開始 \n" +
                                   "/vcn_mute_from [数字] ： [数字]時からVC通知をミュート（デフォルトは24時） \n" +
                                   "/vcn_mute_to[数字] ： [数字]時までVC通知をミュート（デフォルトは6時） \n" +
                                   "/vcn_change_channel ： VC通知チャンネルを変更 \n")

    if command == '/vcn_stop':
        if is_notification == True:
            is_notification = False
        await message.channel.send('VC通知を停止しました')

    if command == '/vcn_start':
        if is_notification == False:
            is_notification = True
        await message.channel.send('VC通知を開始しました')

    if command == '/vcn_mute_from':
        vcn_mute_from = int(message.content.split()[1])
        await message.channel.send('{}時からVC通知をミュートします'.format(message.content.split()[1]))

    if command == '/vcn_mute_to':
        vcn_mute_to = int(message.content.split()[1])
        await message.channel.send('{}時からVC通知をミュート解除します'.format(message.content.split()[1]))

    if command == '/vcn_change_channel':
        vcn_channel = message.channel.id
        await message.channel.send('VC通知チャンネルを#{}に変更しました。'.format(message.channel))


@client.event
async def on_voice_state_update(member, before, after):
    global is_notification
    global vcn_channel
    global vcn_mute_from
    global vcn_mute_to
    if vcn_channel == None:
        vcn_channel = client.guilds[0].text_channels[0].id
    alert_channel = client.get_channel(vcn_channel)
    now_time = datetime.now(pytz.timezone('Asia/Tokyo')).hour
    if is_notification == True and vcn_mute_from >= now_time and vcn_mute_to <= now_time:
        if before.channel is None:
            embed = discord.Embed(
                title="{0}が {1} に参加しました".format(member.nick or member.name, after.channel.name), description="やっほー", color=0xff0000)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)
        elif after.channel is None:
            embed = discord.Embed(
                title="{0}が {1} から抜けました".format(member.nick or member.name,before.channel.name), description="バイバイ", color=0xff0000,)
            embed.set_thumbnail(url=member.avatar_url)
            await alert_channel.send(embed=embed)

client.run(os.environ.get("DISCORD_TOKEN"))

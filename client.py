#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
import discord
from datetime import datetime
import pytz

load_dotenv(override=True)

client = discord.Client()
vcn_channel = 826055515243151380
is_notification = True
vcn_mute_from = 24
vcn_mute_to = 6
msg_join = "やっほー"
msg_leave = "ばいばい"


@client.event
async def on_message(message):
    global vcn_channel
    global is_notification
    global vcn_mute_from
    global vcn_mute_to
    global msg_join
    global msg_leave

    command = ''
    params = ''
    try:
        command = message.content.split()[0]
        params = message.content.split()[1]
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
                                   "/vcn_join_msg [メッセージ]： VC参加通知メッセージを変更 \n" +
                                   "/vcn_leave_msg [メッセージ]： VC退出通知メッセージを変更 \n" +
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

    if command == '/vcn_join_msg':
        msg_join = params
        await message.channel.send('VC入室通知メッセージを {} にしました'.format(msg_join))

    if command == '/vcn_leave_msg':
        msg_leave = params
        await message.channel.send('VC退出通知メッセージを {} にしました'.format(msg_leave))

    if command == '/vcn_mute_from':
        vcn_mute_from = int(params)
        await message.channel.send('{}時からVC通知をミュートします'.format(params))

    if command == '/vcn_mute_to':
        vcn_mute_to = int(params)
        await message.channel.send('{}時からVC通知をミュート解除します'.format(params))

    if command == '/vcn_change_channel':
        vcn_channel = message.channel.id
        await message.channel.send('VC通知チャンネルを#{}に変更しました'.format(message.channel))


@client.event
async def on_voice_state_update(member, before, after):
    # global vcn_channel
    # if vcn_channel == None:
    #     vcn_channel = client.guilds[0].text_channels[0].id
    alert_channel = client.get_channel(vcn_channel)
    now = datetime.now(pytz.timezone('Asia/Tokyo'))
    now_time = now.strftime('%H:%M:%S')
    if is_notification == True and vcn_mute_from >= now.hour and vcn_mute_to <= now.hour:
        if before.channel is None:
            embed = discord.Embed(
                title="{0}が {1} に参加しました".format(member.nick or member.name, after.channel.name), description=msg_join, color=0xff0000)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Time", value=now_time, inline=True)
            embed.add_field(name="Members", value=len(after.channel.voice_states.keys()), inline=True)
            await alert_channel.send(embed=embed)
        elif after.channel is None:
            embed = discord.Embed(
                title="{0}が {1} から抜けました".format(member.nick or member.name, before.channel.name), description=msg_leave, color=0x0000ff)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Time", value=now_time, inline=True)
            embed.add_field(name="Members", value=len(before.channel.voice_states.keys()), inline=True)
            await alert_channel.send(embed=embed)

client.run(os.environ.get("DISCORD_TOKEN"))

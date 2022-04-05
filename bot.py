#                        _oo0oo_
#                       o8888888o
#                       88" . "88
#                       (| -_- |)
#                       0\  =  /0
#                     ___/`---'\___
#                   .' \|     |// '.
#                  / \|||  :  |||// \
#                 / _||||| -:- |||||- \
#                |   | \\  -  /// |   |
#                | \_|  ''\---/''  |_/ |
#                \  .-\__  '-'  ___/-. /
#              ___'. .'  /--.--\  `. .'___
#           ."" '<  `.___\_<|>_/___.' >' "".
#          | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#          \  \ `_.   \_ __\ /__ _/   .-` /  /
#      =====`-.____`.___ \_____/___.-`___.-'=====
#                        `=---='


import numpy as np
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.utils import get
import datetime
import asyncio
from random import randint, getrandbits

from urllib import parse, request
#import re
#Note lib PyNaCl,discord,numpy

#Var
PlayerName = []
Number = []
Mode = 2
Status = False;
Lock = False;
NumLock = 0

#ระบบค้นหาเลขใกล้เคียงที่สุด
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#init กำหนด prefix bot
bot = commands.Bot(command_prefix='lt!', description="Poom Lotto Stem Discord Bot", pm_help = False)

#Start
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def start(ctx, modenum):
    if int(modenum) == 2 or int(modenum) == 3 : #เช็คว่าเลขอยู่ระหว่าง 0-99
        global Status 
        global Mode
        Status = True;
        Mode = int(modenum)
        await ctx.send("เริ่มเล่นหวยได้โดยครั้งนี้เลข " + str(Mode) + " หลัก")
        await ctx.message.add_reaction('✅')
        channel = bot.get_channel(886873924418273291)
        await channel.send("Stem Lotto> ระบบเริ่มเปิดรับหวยแล้ว")
    else:
        await ctx.send("โปรดเลือกเลขที่อยู่ระหว่าง 2-3");
        await ctx.message.add_reaction('❌')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def stop(ctx):
    global Status 
    Status = False;
    await ctx.send("ระบบปิดรับเลขแล้ว โปรดรอลุ้น")
    await ctx.message.add_reaction('✅')
    channel = bot.get_channel(886873924418273291)
    await channel.send("Stem Lotto> ระบบปิดแล้ว")

@bot.command()
async def status(ctx):
    if Status == True:
        await ctx.send("ระบบยังเปิดรับเลขอยู่ รีบพิม lt!buy เลข");
        await ctx.message.add_reaction('✅')
    elif Status == False:
        await ctx.send("ปิดรับเลขแล้ว หรือ ยังไม่ได้เริ่มกิจกรรม");
        await ctx.message.add_reaction('❌')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def reset(ctx):
    global Number
    global PlayerName
    global Lock
    Number.clear()
    PlayerName.clear()
    Lock = False;
    await ctx.send("รีเซ็ตข้อมูลกองเสร็จสิ้น")
    await ctx.message.add_reaction('✅')
    channel = bot.get_channel(886873924418273291)
    await channel.send("Stem Lotto> ระบบรีเซ็ตข้อมูลกองสลากแล้ว")

#Player Select
@bot.command()
async def buy(ctx, numOne):
    global Status
    global Mode
    global Number
    global PlayerName
    if Status == True:
        if Mode == 2:
            SelNum = 0
            Player = str(ctx.message.author.mention)
            if int(numOne) <= 99 and int(numOne) >= 0 : #เช็คว่าเลขอยู่ระหว่าง 0-99
                SelNum = int(numOne)
                if SelNum in Number:
                    await ctx.send("มีคนเลือกเลขก่อนท่านแล้ว โปรดเลือกใหม่");
                    await ctx.message.add_reaction('❌')
                else: 
                    if Player in PlayerName:
                        await ctx.send("ท่านเลือกไปแล้ว ห้ามเปลี่ยน");
                        await ctx.message.add_reaction('❌')
                    else: 
                        Number.append(SelNum)
                        PlayerName.append(str(ctx.message.author.mention))
                        await ctx.send(f"คุณ  {ctx.message.author.mention} เลือกเลข %d"%int(SelNum));
                        await ctx.message.add_reaction('✅')
            else:
                await ctx.send("โปรดเลือกเลขที่อยู่ระหว่าง 00-99");
                await ctx.message.add_reaction('❌')
        elif Mode == 3:
            SelNum = 0
            Player = str(ctx.message.author.mention)
            if int(numOne) <= 999 and int(numOne) >= 0 : #เช็คว่าเลขอยู่ระหว่าง 0-99
                SelNum = int(numOne)
                if SelNum in Number:
                    await ctx.send("มีคนเลือกเลขก่อนท่านแล้ว โปรดเลือกใหม่");
                    await ctx.message.add_reaction('❌')
                else: 
                    if Player in PlayerName:
                        await ctx.send("ท่านเลือกไปแล้ว ห้ามเปลี่ยน");
                        await ctx.message.add_reaction('❌')
                    else: 
                        Number.append(SelNum)
                        PlayerName.append(str(ctx.message.author.mention))
                        await ctx.send(f"คุณ  {ctx.message.author.mention} เลือกเลข %d"%int(SelNum));
                        await ctx.message.add_reaction('✅')
            else:
                await ctx.send("โปรดเลือกเลขที่อยู่ระหว่าง 000-999");
                await ctx.message.add_reaction('❌')
    else:
        await ctx.send("กิจกรรมยังไม่เริ่มใจเย็นๆสิ");
        await ctx.message.add_reaction('❌')

#Check
@bot.command()
async def check(ctx):
    global Number
    global PlayerName
    Player = str(ctx.message.author.mention)
    if Player in PlayerName:
        NumListOfP = PlayerName.index(Player)
        PNumSel = Number[NumListOfP]
        await ctx.send(f"คุณ  {ctx.message.author.mention} ได้เลือกเลข %d"%PNumSel);
        await ctx.message.add_reaction('✅')
    else:
        await ctx.send("ท่านยังไม่ได้เลือกเลข โปรดไปเลือกด้วย");
        await ctx.message.add_reaction('❌')

@bot.command(pass_context=True)
async def amount(ctx):
    global PlayerName
    await ctx.send("มีผู้เล่นทั้งหมด " + str(len(PlayerName)) + " คน");
    await ctx.message.add_reaction('✅')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def listpl(ctx):
    global Number
    global PlayerName
    for y in range(len(PlayerName)):
        await ctx.send("ผู้เล่น " + str(PlayerName[y]) + " ได้เลือกเลข " + str(Number[y]));
    await ctx.message.add_reaction('✅')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def locknum(ctx, numlock):
    global Lock
    global NumLock
    Lock = True;
    NumLock = int(numlock)
    await ctx.send("การกำหนดเลขที่ออกเสร็จสิ้น")
    await ctx.message.add_reaction('✅')
    channel = bot.get_channel(886873924418273291)
    await channel.send("Stem Lotto> ล็อกหวยที่จะออกแล้ว")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def give(ctx, numOne, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    Player = await bot.fetch_user(f"{member.id}")
    global Status
    global Mode
    global Number
    global PlayerName
    if Status == True:
        if Mode == 2:
            SelNum = 0
            if int(numOne) <= 99 and int(numOne) >= 0 : #เช็คว่าเลขอยู่ระหว่าง 0-99
                SelNum = int(numOne)
                if SelNum in Number:
                    await ctx.send("มีคนเลือกเลขก่อนท่านแล้ว โปรดเลือกใหม่");
                    await ctx.message.add_reaction('❌')
                else: 
                    if member in PlayerName:
                        await ctx.send("ท่านเลือกไปแล้ว ห้ามเปลี่ยน");
                        await ctx.message.add_reaction('❌')
                    else: 
                        Number.append(SelNum)
                        PlayerName.append(str(member))
                        await ctx.send(f"คุณ  {member} เลือกเลข %d"%int(SelNum));
                        await ctx.message.add_reaction('✅')
            else:
                await ctx.send("โปรดเลือกเลขที่อยู่ระหว่าง 00-99");
                await ctx.message.add_reaction('❌')
        elif Mode == 3:
            SelNum = 0
            if int(numOne) <= 999 and int(numOne) >= 0 : #เช็คว่าเลขอยู่ระหว่าง 0-99
                SelNum = int(numOne)
                if SelNum in Number:
                    await ctx.send("มีคนเลือกเลขก่อนท่านแล้ว โปรดเลือกใหม่");
                    await ctx.message.add_reaction('❌')
                else: 
                    if member in PlayerName:
                        await ctx.send("ท่านเลือกไปแล้ว ห้ามเปลี่ยน");
                        await ctx.message.add_reaction('❌')
                    else: 
                        Number.append(SelNum)
                        PlayerName.append(str(member))
                        await ctx.send(f"คุณ  {member} เลือกเลข %d"%int(SelNum));
                        await ctx.message.add_reaction('✅')
            else:
                await ctx.send("โปรดเลือกเลขที่อยู่ระหว่าง 000-999");
                await ctx.message.add_reaction('❌')
    else:
        await ctx.send("กิจกรรมยังไม่เริ่มใจเย็นๆสิ");
        await ctx.message.add_reaction('❌')


#Random
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def spin(ctx):
    global Number
    global PlayerName
    global Lock
    global NumLock
    global Mode
    if Lock == True:
        if Mode == 2:
            NumOfRandom = NumLock
            numNear = find_nearest(Number, NumOfRandom)
            PlayerOwnNumList = Number.index(numNear)
            LuckPlayer = PlayerName[PlayerOwnNumList]
            MessageSend = str("หวยประจำวันนี้ เลขที่ออกคือ " + str(NumOfRandom) + " โดยเลขใกล้เคียงสุดคือ " + str(numNear) + " ซึ่งผู้ที่ครอบครองได้แก่ " + str(LuckPlayer))
            Number.remove(numNear)
            PlayerName.remove(LuckPlayer)
            Lock = False;
            await ctx.send(MessageSend)
            await ctx.message.add_reaction('✅')
        elif Mode == 3:
            NumOfRandom = NumLock
            numNear = find_nearest(Number, NumOfRandom)
            PlayerOwnNumList = Number.index(numNear)
            LuckPlayer = PlayerName[PlayerOwnNumList]
            MessageSend = str("หวยประจำวันนี้ เลขที่ออกคือ " + str(NumOfRandom) + " โดยเลขใกล้เคียงสุดคือ " + str(numNear) + " ซึ่งผู้ที่ครอบครองได้แก่ " + str(LuckPlayer))
            Number.remove(numNear)
            PlayerName.remove(LuckPlayer)
            Lock = False;
            await ctx.send(MessageSend)
            await ctx.message.add_reaction('✅')
            
    elif Lock == False:
        if Mode == 2:
            NumOfRandom = randint(0, 99)
            numNear = find_nearest(Number, NumOfRandom)
            PlayerOwnNumList = Number.index(numNear)
            LuckPlayer = PlayerName[PlayerOwnNumList]
            MessageSend = str("หวยประจำวันนี้ เลขที่ออกคือ " + str(NumOfRandom) + " โดยเลขใกล้เคียงสุดคือ " + str(numNear) + " ซึ่งผู้ที่ครอบครองได้แก่ " + str(LuckPlayer))
            Number.remove(numNear)
            PlayerName.remove(LuckPlayer)
            await ctx.send(MessageSend)
            await ctx.message.add_reaction('✅')
        elif Mode == 3:
            NumOfRandom = randint(0, 999)
            numNear = find_nearest(Number, NumOfRandom)
            PlayerOwnNumList = Number.index(numNear)
            LuckPlayer = PlayerName[PlayerOwnNumList]
            MessageSend = str("หวยประจำวันนี้ เลขที่ออกคือ " + str(NumOfRandom) + " โดยเลขใกล้เคียงสุดคือ " + str(numNear) + " ซึ่งผู้ที่ครอบครองได้แก่ " + str(LuckPlayer))
            Number.remove(numNear)
            PlayerName.remove(LuckPlayer)
            await ctx.send(MessageSend)
            await ctx.message.add_reaction('✅')

#Voice
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def vjoin(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()
    
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def vleave(ctx):
    await ctx.voice_client.disconnect()

# Events
@bot.event
async def on_ready():
    #await bot.change_presence(activity=discord.Streaming(name="ภูมิกำลังทำงาน", url="http://memewithyasart.ml"))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="สลากไม่กินโยนงานให้แอดเต้แอดภูมิจะได้ไม่ต้องทำ"))
    print('My bot has ready naja xd.')


@bot.listen()
async def on_message(message):
    if "ยอดเยี่ยมไปเลยนะครับสุดยอดมากเลยฮะ" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
        await message.channel.send('This is that you want http://memewithyasart.ml')
        await bot.process_commands(message)
        await ctx.message.add_reaction('✅')

bot.run("Plese Copy and Paste here")

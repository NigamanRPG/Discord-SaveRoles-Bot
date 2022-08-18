#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import asyncio
import pymysql
import discord
from discord.ext import commands

def load_config():
    """Загрузка конфигурации из JSON"""
    json_config_file = './config/example.json' # Путь до файла с токеном и данными для подключения к mysql
    with open(json_config_file, 'r') as file:
        return json.load(file)

def init():
    global jsonconfig
    jsonconfig = load_config()
    global bot
    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix="$",intents=intents)
    bot.remove_command("help")


if __name__ == '__main__':
    init()

@bot.event
async def on_ready():
    connect = pymysql.connect(jsonconfig["HOSTNAME"], jsonconfig["USERNAME"], jsonconfig["PASSWD"], jsonconfig["DB"])
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS save_state(guild_id TEXT, state TEXT)") # Проверка существования таблиц
    cursor.execute("CREATE TABLE IF NOT EXISTS save_roles(guild_id TEXT, user_id TEXT, roles TEXT)")
    connect.commit()
    cursor.close()
    connect.close()
    print("[MySQL] Таблицы проверены")
    print(f"[CONNECT] Соединение с {bot.user.name}")
    print("[SUCCESS] Бот запущен")  # Вывод информации о запуске
    await bot.change_presence(status=discord.Status.online)

@bot.command(pass_context=True) # Команда для включения функции. Принимаемые аргументы enable/disable
async def save_role(ctx,*, arg=None):
    try:
        author = ctx.message.author
        if author.guild_permissions.administrator:  
            connect = pymysql.connect(jsonconfig["HOSTNAME"], jsonconfig["USERNAME"], jsonconfig["PASSWD"], jsonconfig["DB"])
            cursor = connect.cursor()
            cursor.execute(f"SELECT state FROM save_state WHERE guild_id = {ctx.guild.id}")
            res = cursor.fetchone()            
            if arg == "enable":
                if res is not None:
                    return await ctx.send("bot: Режим сохранения ролей уже включен")
                val = (ctx.guild.id, arg)
                cursor.execute(f"INSERT INTO save_state(guild_id, state) VALUES(%s, %s)", val)
                await ctx.send("bot: Режим сохранения ролей успешно включен") 
            elif arg == "disable":    
                if res is None:
                    return await ctx.send("bot: Режим сохранения ролей уже выключен")     
                    cursor.execute(f"DELETE FROM save_state WHERE {guild_id} = {ctx.guild.id}")           
                    await ctx.send("bot: Режим сохранения ролей успешно выключен")
                else:
                    await ctx.send("bot: Указано неверное значение аргумента")
            connect.commit()
            cursor.close()
            connect.close()               
        else:
            await ctx.send("bot: Недостаточно прав для выполнения команды. Необходимые права: **Администратор**.")
    except:
         await ctx.send("bot: Неизвестная ошибка")


@bot.event
async def on_member_join(member):
    try:
        connect = pymysql.connect(jsonconfig["HOSTNAME"], jsonconfig["USERNAME"], jsonconfig["PASSWD"], jsonconfig["DB"])
        cursor = connect.cursor()
        cursor.execute(f"SELECT state FROM save_state WHERE guild_id = {member.guild.id}")
        res = cursor.fetchone()
        if res is not None:
            cursor.execute(f"SELECT roles FROM save_roles WHERE guild_id = '{member.guild.id}' AND user_id = '{member.id}'")
            res = cursor.fetchone()
            if res is not None:    
                res = str(res[0]).split(",")
                for role in res:
                    await member.add_roles(discord.utils.get(member.guild.roles, id=int(role)))
                    cursor.execute(f"DELETE FROM save_roles WHERE guild_id = '{member.guild.id}' AND user_id = '{member.id}'")
                    connect.commit()
                    cursor.close()
                    connect.close() 
    except:
        pass


@bot.event
async def on_member_remove(member):
    try:
        connect = pymysql.connect(jsonconfig["HOSTNAME"], jsonconfig["USERNAME"], jsonconfig["PASSWD"], jsonconfig["DB"])
        cursor = connect.cursor()
        cursor.execute(f"SELECT state FROM save_state WHERE guild_id = {member.guild.id}")
        res = cursor.fetchone()
        if res is not None:
            user_roles = []
            for role in member.roles:
                user_roles.append(role.id)
            user_roles.remove(member.guild.id) 
            user_roles = str(user_roles).replace('[','').replace(']','')
            cursor.execute(f"SELECT roles FROM save_roles WHERE guild_id = '{member.guild.id}' AND user_id = '{member.id}'")
            res = cursor.fetchone()
            if res == None:
                val = (str(member.guild.id), str(member.id), str(user_roles))                 
                cursor.execute("INSERT INTO save_roles (guild_id, user_id, roles) VALUES(%s, %s, %s)", val)  
            else:
                cursor.execute(f"UPDATE save_roles SET roles = '{user_roles}' WHERE guild_id = '{member.guild.id}' AND user_id = '{member.id}'")
        connect.commit()
    except:
        pass  

bot.run(jsonconfig["TOKEN"]) 
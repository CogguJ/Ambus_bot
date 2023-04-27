import disnake
import random
import requests
import asyncio
from disnake.ext import commands

config = {
    'token': 'TOKEN',
    'prefix': '/',
}

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.slash_command()
async def help(interaction: disnake.AppCmdInter):
    interaction.send("**Данный бот предназначен для базовых работ с сервером**\n"
                     "Почти каждая команда бота описывается при её вызове")


@bot.slash_command(description="Настройка сервера! (ОПАСНО - УДАЛЯЕТ ВСЕ РОЛИ И КАНАЛЫ И СОЗДАЁТ ВСЁ ЗАНОВО)")
@commands.has_permissions(administrator=True)
async def op_guild(interaction: disnake.AppCmdInter, guild: disnake.Guild, ):
    for role in guild.roles:
        try:
            await role.delete(reason="Настройка")
        except:
            pass
    for channel in guild.channels:
        try:
            await channel.delete(reason="Настройка")
        except:
            pass
    ctg1 = await guild.create_category("Текстовики")
    await guild.create_text_channel("Новости", category=ctg1)
    await guild.create_text_channel("Говорильня", category=ctg1)
    await guild.create_text_channel("Поиск игроков", category=ctg1)
    ctg2 = await guild.create_category("Голосовики")
    await guild.create_voice_channel("bla-bla-bla", category=ctg2)
    ctg3 = await guild.create_category("AFK")
    await guild.create_voice_channel("AFK -Zzzz-", category=ctg3)
    await guild.create_role(name="♂")
    await guild.create_role(name="♀")
    ych = await guild.create_role(name="Участник")
    for member in guild.members:
        await member.add_roles(ych)


@bot.event
async def on_message(message):
    kot = ["котики", "кошечка", "кися", "мурлыка", 'кот', 'коты', 'кошечки', 'котэ', "котик"]
    dog = ["пёсики", "cобачки", "псина", "гавкалка", 'пёс', 'собачка', 'собачки', "пёсик"]
    if "set_timer" in message.content.lower():
        x = message.content.lower().split()
        h, m = 0, 0
        for i in range(len(x)):
            if x[i] == "hours":
                h = x[i - 1]
            if x[i] == "minutes":
                m = x[i - 1]
        sec = (int(h) * 3600) + (int(m) * 60)
        await message.channel.send(f":alarm_clock: Timer start {m} minutes and {h} hours")
        while sec != 0:
            sec -= 1
            await asyncio.sleep(0.99)
        await message.channel.send(":alarm_clock: TIME X HAS COME")
    if message.content.lower() in kot:
        r = requests.get('https://api.thecatapi.com/v1/images/search').json()
        await message.channel.send(r[0]['url'])
    if message.content.lower() in dog:
        r = requests.get('https://dog.ceo/api/breeds/image/random').json()
        await message.channel.send(r['message'])


@bot.slash_command(description="очистка чата от amount сообщений (стандартно 10)")
@commands.has_permissions(administrator=True)
async def clear(interaction: disnake.AppCmdInter, amount=10):
    await interaction.channel.purge(limit=amount)
    await interaction.send("!Удаление!")


@bot.slash_command()
@commands.has_permissions(administrator=True)
async def test(interaction: disnake.AppCmdInter, guild: disnake.Guild):
    await interaction.send("ХАХАХАХА")
    ctg1 = await guild.create_category("Текстовики")
    await guild.create_text_channel("Новости", category=ctg1)
    ctg2 = await guild.create_category("Голосовики")
    await guild.create_voice_channel("bla-bla-bla", category=ctg2)


@bot.slash_command(description="кик пользователя")
@commands.has_permissions(administrator=True)
async def kick(interaction: disnake.AppCmdInter, user: disnake.Member, *arg, reason='Причина не указана'):
    await bot.kick(user)
    await interaction.send(f'Пользователь {user.name} был изгнан по причине "{reason}"')


@bot.slash_command(description="рандомное число от MIN до MAX")
async def rand(interaction: disnake.AppCmdInter, min='1', max='100'):
    if min.isdigit() and max.isdigit():
        await interaction.send(random.randint(int(min), int(max)))
    else:
        await interaction.send("неверные аргументы -_-")


@bot.slash_command(name="role")
@commands.has_permissions(administrator=True)
async def role(interaction: disnake.AppCmdInter, member: disnake.Member, *, role: disnake.Role):
    await member.add_roles(role)
    await interaction.send(f'роль "*{role}*" добавлена')


@bot.slash_command(description="Статистика сервера")
async def server_stat(inter):
    await inter.response.send_message(
        f"Название сервера: {inter.guild.name}\nВсего участников: {inter.guild.member_count}"
    )


bot.run(config['token'])

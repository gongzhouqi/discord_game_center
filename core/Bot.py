from discord import FFmpegPCMAudio, FFmpegOpusAudio
from discord.ext import commands

from core.Exception import *
import core.Games.Library
from core.Hall import Hall

bot = commands.Bot(command_prefix='-')
voice_connection = None

hall = Hall()

# my id
my_id = 362428898329362433


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="创建")
async def create_room(ctx, *args):
    if len(args) != 1:
        await ctx.send("创建命令仅支持一个参数。\n-创建 【游戏名】")
    else:
        game_name = args[0]
        try:
            hall.create_room(ctx.author, ctx.channel, game_name)
            await ctx.send("{} 创建了{}房间。".format(str(ctx.author), game_name))
        except NoSuchGameException:
            await ctx.send("{} 创建房间失败，没有这个游戏。用 \"-游戏表\" 来查看所有游戏。".format(str(ctx.author)))
        except ChannelOccupiedException:
            await ctx.send("{} 创建房间失败，每个频道只能有一个活动中的房间。".format(str(ctx.author)))
        except PlayerOccupiedException:
            await ctx.send("{} 创建房间失败，请先退出之前的房间。".format(str(ctx.author)))
        except Exception as e:
            await ctx.send(str(e))


@bot.command(name="游戏表")
async def game_list(ctx):
    res = "\n".join(core.Games.Library.games.keys())
    await ctx.send(res)


@bot.command(name="加入")
async def join(ctx):
    try:
        hall.join_room(ctx.author, ctx.channel)
        await ctx.send("{} 加入了房间。".format(str(ctx.author)))
    except PlayerOccupiedException:
        await ctx.send("{} 加入房间失败，请先退出之前的房间。".format(str(ctx.author)))
    except NoSuchRoomException:
        await ctx.send("{} 加入房间失败，该频道没有活动中的房间。".format(str(ctx.author)))
    except InGamingException:
        await ctx.send("{} 加入房间失败，正在游戏中。".format(str(ctx.author)))
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name="退出")
async def leave(ctx):
    try:
        hall.leave_room(ctx.author, ctx.channel)
        await ctx.send("{} 退出了房间。".format(str(ctx.author)))
    except PlayerNotInRoomException:
        await ctx.send("{} 退出房间失败，并不在该频道的房间中。".format(str(ctx.author)))
    except NoSuchRoomException:
        await ctx.send("{} 退出房间失败，该频道没有活动中的房间。".format(str(ctx.author)))
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name="关闭")
async def close_room(ctx):
    try:
        hall.close_room(ctx.author, ctx.channel)
        await ctx.send("{} 关闭了房间。".format(str(ctx.author)))
    except NoSuchRoomException:
        await ctx.send("{} 关闭房间失败，该频道没有活动中的房间。".format(str(ctx.author)))
    except NotOwnerException as e:
        owner = e.args[0]
        await ctx.send("{} 关闭房间失败，只有房主 {} 可以关闭房间。".format(str(ctx.author), str(owner)))
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name="开始")
async def start_game(ctx):
    try:
        hall.start_room_game(ctx.author, ctx.channel)
    except NoSuchRoomException:
        await ctx.send("{} 启动游戏失败，该频道没有活动中的房间。".format(str(ctx.author)))
    except NotOwnerException as e:
        owner = e.args[0]
        await ctx.send("{} 启动游戏失败，只有房主 {} 可以启动游戏。".format(str(ctx.author), str(owner)))
    except InGamingException:
        await ctx.send("{} 启动游戏失败，房间已经在游戏中。".format(str(ctx.author)))
    except GamePopulationException as e:
        args = e.args
        await ctx.send("{} 启动游戏失败，{}仅支持{}到{}人游玩。".format(str(ctx.author), args[0], args[1], args[2]))
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name="设置")
async def setting(ctx, arg):
    # TODO: 游戏设置
    pass


@bot.command(name="i")
async def play_game(ctx, *args):
    try:
        hall.pass_instruction_to_game(ctx.author, ctx.channel, args)
    except NoSuchRoomException:
        await ctx.send("{} 输入游戏指令失败，该频道没有活动中的房间。".format(str(ctx.author)))
    except NotInGamingException:
        await ctx.send("{} 输入游戏指令失败，房间还不在游戏中。".format(str(ctx.author)))
    except GamePlayException as e:
        await ctx.send("Game: {}".format(e.args[0]))
    except Exception as e:
        await ctx.send(str(e))


@bot.command(name="c")
async def play_game(ctx, arg):
    channel = ctx.author.voice.channel
    global voice_connection
    if voice_connection is None:
        voice_connection = await channel.connect()
    if arg == "help":
        pass
    elif arg == "list":
        pass
    elif arg == "1":
        audio = FFmpegOpusAudio(executable=r"D:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                                source=r"D:\Projects\DiscordBots\GameCenter\resource\chat_wheel\sorewadogana.mp3")
        voice_connection.play(audio)
    elif arg == "2":
        audio = FFmpegOpusAudio(executable=r"D:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                                source=r"D:\Projects\DiscordBots\GameCenter\resource\chat_wheel\fight_five.mp3")
        voice_connection.play(audio)
    elif arg == "3":
        audio = FFmpegOpusAudio(executable=r"D:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                                source=r"D:\Projects\DiscordBots\GameCenter\resource\chat_wheel\omayiwamoxindeyilu.mp3")
        voice_connection.play(audio)
    elif arg == "4":
        audio = FFmpegOpusAudio(executable=r"D:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                                source=r"D:\Projects\DiscordBots\GameCenter\resource\chat_wheel\awooo.mp3")
        voice_connection.play(audio)


@bot.command()
async def BGM(ctx):
    chn = ctx.author.voice.channel
    connection = await chn.connect()
    audio = FFmpegPCMAudio(executable=r"D:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
                           source=r"D:\Projects\DiscordBots\GameCenter\core\songs\夜曲.mp3")
    connection.play(audio)


@bot.command()
async def test(ctx):
    msg = ctx.message
    await msg.delete()


# async def _after_test():


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))

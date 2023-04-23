from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('help', 'Список всех команд'),
            BotCommand('company', 'Информация о компании'),
            BotCommand('faq', 'Ответы на частые вопросы'),
        ],
        scope=BotCommandScopeDefault()
    )

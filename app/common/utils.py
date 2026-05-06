from aiogram.enums import ParseMode


async def notify_target_user(bot, target_id, msg, button_data=None):
    await bot.send_message(target_id, msg,
                           reply_markup=button_data, parse_mode=ParseMode.HTML)

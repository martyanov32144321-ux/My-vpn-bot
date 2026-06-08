import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

# Твой токен бота и ссылка на тебя
BOT_TOKEN = "8922941146:AAF-2VvSxl7sRFX0BgOCyx70bOwksWiJWek"
SUPPORT_LINK = "https://t.me/legdarknez"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile"))
    keyboard.row(types.InlineKeyboardButton(text="🚀 Получить VPN (Тест)", callback_data="get_vpn"))
    keyboard.row(types.InlineKeyboardButton(text="💳 Продлить подписку / Тарифы", callback_data="rates"))
    keyboard.row(types.InlineKeyboardButton(text="📱 Как подключить (Инструкция)", callback_data="instruction"))
    keyboard.row(types.InlineKeyboardButton(text="👨‍💻 Техподдержка", url=SUPPORT_LINK))
    return keyboard.as_markup()

def back_button():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(types.InlineKeyboardButton(text="⬅️ В главное меню", callback_data="to_main"))
    return keyboard.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    photo_url = "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?q=80&w=1000"
    await message.answer_photo(
        photo=photo_url,
        caption=(
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            f"Добро пожаловать в твой личный, приватный и самый быстрый VPN.\n\n"
            f"• Идеально работает на мобильном интернете (4G/LTE/5G).\n"
            f"• Не режет скорость и не тратит батарею.\n"
            f"• Полная конфиденциальность ваших данных.\n\n"
            f"Управлять подпиской и получить настройки можно через меню ниже 👇"
        ),
        reply_markup=main_menu()
    )

@dp.callback_query(lambda c: c.data == "my_profile")
async def process_profile(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name
    username = callback_query.from_user.username or "не установлен"
    
    await callback_query.message.answer(
        f"👤 **Твой профиль VPN**\n\n"
        f"• **Имя:** {first_name}\n"
        f"• **Юзернейм:** @{username}\n"
        f"• **Твой ID:** `{user_id}`\n\n"
        f"• 🟢 **Статус подписки:** Активна (Тестовый период)\n"
        f"• 📅 **Действует до:** 15.06.2026",
        parse_mode="Markdown",
        reply_markup=back_button()
    )
    await callback_query.message.delete()
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "get_vpn")
async def process_get_vpn(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "🎁 **Твой тестовый период активирован!**\n\n"
        "Мы дарим тебе бесплатный доступ, чтобы ты лично проверил космическую скорость нашего VPN.\n\n"
        "🔑 **Твой ключ доступа:**\n"
        "`vless://test-key-will-be-here-after-setup-reality` \n\n"
        "*(Нажми на ключ выше, чтобы он автоматически скопировался)*.\n\n"
        "👉 Перейди в раздел «Как подключить» в главном меню, чтобы вставить этот ключ в приложение.",
        parse_mode="Markdown",
        reply_markup=back_button()
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "rates")
async def process_rates(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "💳 **Наши тарифы и подписка**\n\n"
        "У нас нет ограничений по трафику и скорости. Выбирай любой удобный период:\n\n"
        "• 📅 1 месяц — 250 рублей\n"
        "• 📅 3 месяца — 650 рублей *(Экономия 100₽)*\n"
        "• 📅 6 месяцев — 1200 рублей *(Экономия 300₽)*\n\n"
        "💬 Для продления или покупки подписки напиши нашему администратору в раздел «Техподдержка». Скоро здесь будет автоматическая оплата!",
        reply_markup=back_button()
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "instruction")
async def process_instruction(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "📱 **Инструкция по настройке VPN**\n\n"
        "**Для iPhone / iPad:**\n"
        "1. Скачай из App Store бесплатное приложение FoXray или v2rayNG.\n"
        "2. Скопируй свой ключ из раздела «Получить VPN».\n"
        "3. Открой приложение, нажми значок «+» или «Clipboard» (вставить из буфера) и добавь ключ.\n"
        "4. Нажми кнопку подключения (Play/Старт).\n\n"
        "**Для Android:**\n"
        "1. Скачай из Google Play приложение v2rayNG.\n"
        "2. Скопируй ключ, нажми «+» в приложении -> «Импортировать профиль из буфера обмена».\n"
        "3. Выбери добавленный профиль и нажми круглую кнопку подключения внизу.",
        parse_mode="Markdown", 
        reply_markup=back_button()
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "to_main")
async def process_to_main(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "👋 Выберите интересующий раздел ниже, чтобы управлять своим VPN:",
        reply_markup=main_menu()
    )
    await callback_query.message.delete()
    await callback_query.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

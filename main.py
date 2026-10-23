
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart  
from aiogram.types import Message
from dotenv import load_dotenv
import asyncio
import os
from connection import *
from service import *
from keyboard import *

load_dotenv()

token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    user = message.from_user

    if await get_user(user.id):
        await message.answer(
            f"Hello, MRS | MR {user.username}"
        )
        await message.answer(
            f"Mr | Mrs @{user.username} for seeing all comands enter /help",
            reply_markup=main_menu()
        )
    else:
        await created_user(user.username, user.full_name, 0, user.id)
        await message.answer(
            f"Hello @{user.username} how are you ?",
            reply_markup=main_menu()
        )


@dp.message(Command("help"))
@dp.message(F.text == "Help")
async def help_command(message: Message):
    await message.answer(
        "Welcome! Here are the available commands:\n\n"
        "/start — Start the bot\n"
        "/help — Show help\n"
        "/profile — View your profile\n"
        "/history — Transaction history\n"
        "/deposit — Add income\n"
        "/withdraw — Add expense\n"
        "/goal — Goals and debts\n"
        "/pogoshenia — Repay a debt"
    )


@dp.message(Command("profile"))
@dp.message(F.text == "Profile")
async def profile(message: Message):
    print("Profile command received")
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("User not found. Enter /start.")
        return
    await message.answer(
        f"👤 Full Name: {user['full_name']}\n"
        f"🏷 Username: @{user['username']}\n"
        f"💳 Balance: {user['balance']} TJS"
    )



@dp.message(Command("history"))
@dp.message(F.text == "History")
async def history(message: Message):
    transactions = await get_history(message.from_user.id)

    if not transactions:
        await message.answer("History is empty.")
    text = "Transaction History:\n\n"
    for i in transactions:
        text += (
            f"{i['type']}: {i['amount']} TJS\n"
            f"Category: {i['category']}\n\n"
        )

    await message.answer(text)



@dp.message(Command("deposit"))
async def deposit(message: Message):
    await message.answer("Enter earned amount in TJS:")


@dp.message(Command("withdraw"))
async def withdraw(message: Message):
    await message.answer("Enter raskhod amount in TJS:")


@dp.message(Command("goal"))
async def goal(message: Message):
    await message.answer(
        "Goals and debts:\n"
        "To create a goal, enter /newgoal\n"
        "To add a debt, enter /newdebt"
    )


@dp.message(Command("pogoshenia"))
async def pogoshenia(message: Message):
    await message.answer("Enter the debt ID you want to repay:")


async def main():
    await create_table()
    print("Bot started successfully")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
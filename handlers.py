# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton  # типы
from aiogram.filters import Command  # фильтры


# Свои модули
import text  # тексты сообщений
import utils  # общие утилиты
# import sql_utils  # утилиты работы с бд
# from keyboard import CallbackData
# import keyboard  # клавиатуры и inline кнопки


# aiogram FSM модуль
import states  # свой модули с состояниями
from aiogram.fsm.context import FSMContext  # управление состояниями


router = Router()


''' - - - - - - - IMPORTANT HANDLERS - - - - - - - '''


@router.message(Command("cancel"))
async def check_points_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer_sticker(text.Debug.clear_states_sticker)


''' - - - - - - - FSM HANDLERS - - - - - - - '''


@router.message(states.Registration.name)
async def state_name_handler(msg: Message, state: FSMContext):
    if utils.validate_name(msg.text):
        await state.set_data(msg.text)
        await state.set_state(states.Registration.group)
        await msg.answer(text.Registration.successful_name)
    else:
        await msg.answer_sticker(text.Registration.error_name_sticker)
        await msg.answer(text.Registration.error_name_text)


@router.message(states.Registration.group)
async def state_group_handler(msg: Message, state: FSMContext):
    if utils.validate_group:
        await state.set_data(msg.text)
        utils.add_user_to_bd(state.get_data())
        await msg.answer(text)
    else:
        await msg.answer(text.Registration.error_group_sticker)
        
        

@router.message(Command("check_points"))
async def check_points_handler(msg: Message):
    points = utils.check_points(msg.from_user.id)


"""------- SECRET HANDLER -----"""


@router.message(F.text.lower() == 'мяу')
async def secret_handler(msg: Message):
    await msg.answer("гав")


"""------- OTHER HANDLERS ------"""


@router.message(Command("start")) # при /start проверяем есть ли чел в базе данных
@router.message()
async def start_handler(msg: Message, state: FSMContext):
    # check user
    try:
        check_status = utils.check_user(msg.from_user.id)
        if check_status == None:
            error_message, sticker_id = text.Errors.no_in_bd(msg.from_user.username)
            await msg.answer(error_message)
            await msg.answer_sticker(sticker=sticker_id)
            await state.set_state(states.Registration.name)

    except Exception:
        await msg.answer(text.Errors.er_in_db)

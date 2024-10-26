# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton  # типы
from aiogram.filters import Command  # фильтры
from dulwich.porcelain import reset
from urllib3.util.url import url_attrs

# Свои модули
import keyboard
import text  # тексты сообщений
import utils  # общие утилиты



# aiogram FSM модуль
import states  # свой модули с состояниями
from aiogram.fsm.context import FSMContext  # управление состояниями


router = Router()


''' - - - - - - - IMPORTANT HANDLERS - - - - - - - '''
@router.message(Command("cancel"))
@router.message(F.text == text.Buttons.cancel)
async def cancel_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer_sticker(text.Debug.clear_states_sticker,
                             reply_markup=utils.choose_keyboard(msg.from_user.id))


@router.message(Command("start")) # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message, state: FSMContext):
    try:
        check_status = utils.check_user(msg.from_user.id)
        if check_status is None:
            error_message, sticker_id = text.no_in_bd(msg.from_user.username)
            await msg.answer(error_message)
            await state.set_state(states.Registration.user_name)
            await msg.answer_sticker(sticker_id, reply_markup=keyboard.in_state_kb)
        else:
            await msg.answer(text.Registration.already_in_db,
                             reply_markup=utils.choose_keyboard(tg_user_id=msg.from_user.id))

    except Exception as ex:
        await msg.answer(text.Errors.er_in_db)


''' - - - - - - - FSM HANDLERS - - - - - - - '''
@router.message(states.Registration.user_name)
async def state_name_handler(msg: Message, state: FSMContext):
    try:
        if utils.validate_name(msg.text):
            await state.update_data(user_name=msg.text)
            await state.set_state(states.Registration.user_group)
            await msg.answer(text.Registration.successful_name)
        else:
            await msg.answer_sticker(text.Registration.error_name_sticker)
            await msg.answer(text.Registration.error_name_text)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(states.Registration.user_group)
async def state_group_handler(msg: Message, state: FSMContext):
    try:
        if utils.validate_group(msg.text):
            await state.update_data(group=msg.text)
            data = await state.get_data()
            utils.add_user_to_bd(data, msg.from_user.id, msg.from_user.username)
            await state.clear()
            await msg.answer_sticker(text.Registration.success_sticker,
                                     reply_markup=utils.choose_keyboard(msg.from_user.id))
        else:
            await msg.answer_sticker(text.Registration.error_group_sticker)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)
        

""" ---- ADMIN COMMANDS ---- """
@router.message(Command("admin_key"))
async def admin_key_handler(msg: Message):
    try:
        result = utils.admin_key(msg.text[11:], msg.from_user.id)
        if result:
            await msg.answer(text.Debug.success_admin_key,
                             reply_markup=utils.choose_keyboard(is_admin=True))
        else:
            await msg.answer(text.Debug.invalid_admin_key)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(Command("add_points"))
@router.message(F.text == text.Buttons.add_points)
async def add_points_handler(msg: Message, state:FSMContext):
    try:
        if utils.check_user(msg.from_user.id) == "Admin":
            await msg.answer(text.Admin.add_points_name,
                             reply_markup=keyboard.in_state_kb)
            await state.set_state(states.AddPoints.tg_member_id)
        else:
            await msg.answer(text.Errors.no_permissions)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(states.AddPoints.tg_member_id)
async def add_points_name_handler(msg: Message, state: FSMContext):
    try:
        if utils.validate_name(msg.text):
            tg_member_id = utils.name_in_db(msg.text)
            if tg_member_id is not False:
                await state.update_data(tg_member_id=tg_member_id)
                await state.set_state(states.AddPoints.points_type)
                await msg.answer(text.Admin.add_points_category)
            else:
                await msg.answer(text.Admin.invalid_name)
        else:
            await msg.answer(text.Admin.invalid_name)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(states.AddPoints.points_type)
async def add_points_type_handler(msg: Message, state:FSMContext):
    try:
        result = utils.validate_type(msg.text)
        if result:
            await state.update_data(points_type=msg.text)
            await state.set_state(states.AddPoints.num)
            await msg.answer(text.Admin.add_points_num)
        else:
            await msg.answer(text.Admin.invalid_type)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(states.AddPoints.num)
async def add_num_points_handler(msg: Message, state:FSMContext):
    try:
        result = utils.validate_num(msg.text)
        if result:
            await state.update_data(num=int(msg.text))
            data = await state.get_data()
            utils.add_points_to_user(data, msg.from_user.username)
            await state.clear()
            await msg.answer_sticker(text.Admin.success_add_points_sticker,
                                     reply_markup=utils.choose_keyboard(msg.from_user.id))
        else:
            await msg.answer(text.Admin.invalid_num)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


"""------- SECRET HANDLER -----"""
@router.message(F.text.lower() == 'мяу')
async def secret_handler(msg: Message):
    await msg.answer("гав")


"""------- OTHER HANDLERS ------"""
@router.message(Command("check_points"))
@router.message(F.text == text.Buttons.check_points)
async def check_points_handler(msg: Message):
    try:
        points = utils.check_points(msg.from_user.id)
        await msg.answer(points)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(Command("check_history"))
@router.message(F.text == text.Buttons.history)
async def history_handler(msg: Message):
    try:
        result = utils.check_history(msg.from_user.id)
        await msg.answer(result)

    except Exception as exp:
        utils.print_err_in_console(exp)
        await msg.answer(text.Errors.unnamed_er)


@router.message(Command("help"))
async def history_handler(msg: Message):
    await msg.answer_sticker(text.Debug.help_sticker)


@router.message()
async def other_handler(msg: Message, state: FSMContext):
    await start_handler(msg, state)

import keyboard
import text
import regex
import datetime
from os import getenv
from dotenv import load_dotenv

import sql_utils


def print_err_in_console(exp):
    print('-------- ERROR -----------')
    print(exp)
    print('-------- ERROR -----------')


def check_user(tg_user_id: int):
    """
    Берет tg_user_id и возвращает:
    None - если пользователя нет в БД
    True - если в БД есть
    "ADMIN" - если пользователь имеет статус админа
    """
    records = sql_utils.check_user_in_bd(tg_user_id)
    if records:
        if records[0][-1] == 1:
            return "Admin"
        return True
    return None


def check_points(tg_user_id: int):
    """
    Берет tg_user_id и возвращает:
    tech - инженерные баллы
    art  - творческие баллы
    """
    records = sql_utils.check_user_in_bd(tg_user_id)
    tech, art = records[0][4], records[0][5]
    result = text.generate_points_text(tech, art)
    return result


def check_history(tg_user_id: int):
    records = sql_utils.check_history_in_db(tg_user_id)

    if records:
        result = ''
        for i in range(len(records)):
            line = records[i]
            date = line[4]
            if line[1]:
                delta_points = line[1]
                delta_type = 'инженерных'
            else:
                delta_points = line[2]
                delta_type = 'творческих'
            result += f'{i + 1:>2}. Админом {line[3]} начислено {delta_type} баллов: {delta_points} датой от {date}.\n'
        return result
    return "История пуста"


def check_is_rus_word(word):
    """
    Берет name и возвращает:
    True - все символы - русские или тире
    False - иначе
    """
    
    rus_a, rus_ya = 1072, 1103
    for symbol in word:
        if (ord(symbol.lower()) > rus_ya or ord(symbol.lower()) < rus_a) and symbol != '-':
            return False
    return True


def validate_name(name: str) -> bool:
    """
    Берет name и возвращает:\n
    True - имя прошло проверку\n
    False  - имя не прошло проверку
    """
    name_split = name.strip().split()
    if len(name_split) >= 2:
        print(name, all([check_is_rus_word(word) for word in name_split]))
        return all([check_is_rus_word(word) for word in name_split])
    return False


def validate_type(points_type: str):
    return points_type in ('1', '2')


def validate_num(num: str):
    return num.isalnum() and (1 <= int(num) <= 5)


def name_in_db(user_name: str):
    records = sql_utils.user_by_user_name(user_name)
    if records:
        return records[0][0]
    return False


def validate_group(group_name: str) -> bool:
    """
    Берет group и возвращает:\n
    True - группа прошла проверку\n
    False  - группа не прошла проверку
    """
    correct_faculties = [
            'АК', 'БМТ', 'ИБМ', 'ИСОТ', 'ИУ', "Л", 'МТ', 'ОЭ', 'ПС', 'СГН', 'СМ',
            'ТБД', 'ФН', 'РК', 'РКТ' ,'РЛ' ,'РТ' ,'Э', 'ЮР', 'ИУК', 'ИК', 'ПОДК',
            'К', 'ЛТ', 'ТБД', 'ТД', 'ТИП', 'ТМО', 'ТМП', 'ТМР', 'ТР' ,'ТСА', 'ТСР',
            'ТСС', 'ТУ', 'ТУС', 'ТЭ']

    for faculty in correct_faculties:
        if group_name.startswith(faculty):
            matched = regex.match(r'[1-9][0-4]?И?\-1?[1-9][1-9](?:Б|А|М)?', group_name[len(faculty):])
            if matched and len(group_name[len(faculty):]) > 3 and matched.group() == group_name[len(faculty):]:
                return True
            return False
    return False


def add_user_to_bd(data: dict, tg_user_id: int, tg_username: str):
    sql_utils.add_user_in_db(tg_user_id, tg_username, data['user_name'], data['group'])


def choose_keyboard(tg_user_id: int = 0, is_admin=False):
    if is_admin or check_user(tg_user_id) == 'Admin':
        return keyboard.make_kb(is_admin=True)
    return keyboard.make_kb(is_admin=False)


def admin_key(key, tg_user_id):
    load_dotenv(dotenv_path=".env")
    if key == getenv('SECRET_ADMIN_KEY'):
        sql_utils.make_user_admin(tg_user_id)
        return True
    return False


def add_points_to_user(data: dict, tg_admin_name: str):
    date = datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')
    tech_points_delta, art_points_delta = 0, 0
    '''
    tg_member_id = State()
    points_type = State()
    num = State()
    '''
    if data['points_type'] == '1':
        tech_points_delta = data["num"]
    else:
        art_points_delta = data["num"]

    sql_utils.add_points_to_user(data["tg_member_id"], tech_points_delta, art_points_delta, tg_admin_name, date)


if __name__ == '__main__':
    print(check_user(321138226))
import text
import regex

def check_user(tg_user_id: int):
    '''
    Берет tg_user_id и возвращает:
    None    - если пользователя нет в БД
    True    - если в БД есть
    "ADMIN" - если пользователь имеет статус админа
    ''' 
    return None


def check_points(tg_user_id):
    """
    Берет tg_user_id и возвращает:
    tech - инженерные баллы
    art  - творческие баллы
    """
    tech, art = 0, 0 # заглушка
    result = text.generate_points_text     
    return tech, art


def check_is_rus_text(text):
    '''
    Берет name и возвращает:
    True - все символы - русские или тире
    False  - иначе
    '''
    
    rus_a, rus_ya = 1072, 1103
    for symbol in text:
        if (symbol > 1103 or symbol < 1072) and symbol != '-':
            return False
    return True
    


def validate_name(name: str) -> bool:
    '''
    Берет name и возвращает:\n
    True - имя прошло проверку\n
    False  - имя не прошло проверку
    '''
    name_split = name.strip().split()
    if len(name_split) >= 2:
        return all([check_is_rus_text(word) for word in name_split])
    return False


def validate_group(group_name: str) -> bool:
    '''
    Берет group и возвращает:\n
    True - группа прошла проверку\n
    False  - группа не прошла проверку
    '''
    correct_faculties = [
            'АК', 'БМТ', 'ИБМ', 'ИСОТ', 'ИУ', "Л", 'МТ', 'ОЭ', 'ПС', 'СГН', 'СМ',
            'ТБД', 'ФН', 'РК', 'РКТ' ,'РЛ' ,'РТ' ,'Э', 'ЮР', 'ИУК', 'ИК', 'ПОДК',
            'К', 'ЛТ', 'ТБД', 'ТД', 'ТИП', 'ТМО', 'ТМП', 'ТМР', 'ТР' ,'ТСА', 'ТСР',
            'ТСС', 'ТУ', 'ТУС', 'ТЭ']

    for faculty in correct_faculties:
        if group_name.startswith(faculty):
            matched = regex.match(r'\dИ?\-1?\d\d(?:Б|А|М)?', group_name[len(faculty):]).group()
            if matched == group_name[len(faculty):]:
                return True
    return False


def add_user_to_bd(data):
    pass

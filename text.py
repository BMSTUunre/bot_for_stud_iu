class Errors:
    er_in_db = 'Произошла ошибка при работе с БД, обратитесь в дурку.'
    unnamed_er = 'Произошла неинициализированная ошибка, обратитесь в дурку.'
    no_permissions = 'ты не админ.'


class Buttons:
    cancel = '⤫Cancel action'
    add_points = '＋Add points'
    check_points = '🖈Check points'
    history = '⏲History'


class Registration:
    successful_name = 'Допустим, а откуда вы такой ... своеобразный, из какой группы?'
    error_name_sticker = 'CAACAgIAAxkBAAKFQ2caGS6ev6eXUwq2iUQdSWPE_AxwAALeJQAC4t4RSKM1yvvWC1DmNgQ'
    error_name_text = 'что насчет русских буков и 2+ слов?'
    successful_group = 'Ааааа..., та самая группа'
    error_group_sticker = 'CAACAgIAAxkBAAKFXWcbpfSU8_oIUeG0EYKKZGzEFhHLAAKDQAAC1YIBSEfrXWbqHIFjNgQ'
    success_sticker = 'CAACAgIAAxkBAAKFd2cb_l4Y_PuMcRj7GZWZlOHfjLocAALhIwACVJcRSBwJsKXftfUvNgQ'
    already_in_db = 'Оп, к сожалению, о вас я наслышан.'


class Debug:
    clear_states_sticker = 'CAACAgIAAxkBAAKFWmcbeRat3RWROyArsNln2OrKecIxAAKYIgACHuMRSHuQUoy3_lq1NgQ'
    success_admin_key = 'IDKFA.'
    invalid_admin_key = 'Даже не пытайся, не олду не догадаться.'
    help_sticker = 'CAACAgIAAxkBAAKFk2cdVgKbGZaqTvZRw8xU7LFk-pCJAALkIgAC83AQSCDHwxrtuW3JNgQ'


class Admin:
    add_points_name = 'НУ и кого мы так любим? назови фамилию и имя'
    add_points_num = 'И насколько по 5и бальной шкале он вам дорог?'
    add_points_category = 'А чем он так хорош?\n1 - инженерынми навыками\nили\n2 - творческими?'
    invalid_name = 'Нет такого пользователя, попробуй еще.'
    invalid_type = 'Бро, выбрать между 1 и 2 не так тяжело.'
    invalid_num = 'Циферки некрасивые.'
    success_add_points_sticker = 'CAACAgIAAxkBAAKFd2cb_l4Y_PuMcRj7GZWZlOHfjLocAALhIwACVJcRSBwJsKXftfUvNgQ'


def no_in_bd(tg_username: str):
    sticker_id = 'CAACAgIAAxkBAAKFSWcaHD1wuD1hDX9OV32FoGKihgHgAAK6XgACss_hS2W6UCZcul39NgQ'
    error_text = f'Извините {tg_username}, мы кажется незнакомы.'
    return error_text, sticker_id


def generate_points_text(tech_points, art_points):
    if tech_points == 0:
        result = 'У вас нет инженерных баллов.\n'
    else:
        result = f'Количество инженерных баллов: {tech_points}.\n'
    
    if art_points == 0:
        result += 'У вас нет творческих баллов.'
    else:
        result += f'Количество творческих баллов: {art_points}.'
    
    return result


if __name__ == '__main__':
    pass